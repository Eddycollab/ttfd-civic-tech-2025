"""
測試存取控制 (Access Control) 安全性
驗證 save_proof_photo() 函數的權限檢查是否正確運作
"""
import sys
import os
import unittest
import tempfile
from io import BytesIO
from PIL import Image

# 將專案根目錄加入 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db_manager
import utils


class TestAccessControl(unittest.TestCase):
    """測試存取控制功能"""

    @classmethod
    def setUpClass(cls):
        """測試前準備：建立測試資料庫"""
        # 使用臨時資料庫
        cls.original_db = db_manager.DB_NAME
        cls.test_db = "test_access_control.db"
        db_manager.DB_NAME = cls.test_db
        
        # 初始化資料庫
        db_manager.init_db()
        
        # 建立測試資料
        cls._setup_test_data()

    @classmethod
    def tearDownClass(cls):
        """測試後清理：刪除測試資料庫"""
        db_manager.DB_NAME = cls.original_db
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
        
        # 清理測試產生的照片
        test_upload_dir = "uploads/delivery_proofs"
        if os.path.exists(test_upload_dir):
            import shutil
            shutil.rmtree(test_upload_dir)

    @classmethod
    def _setup_test_data(cls):
        """建立測試用的路線、任務和使用者"""
        # 建立送餐路線
        route_id = db_manager.create_delivery_route("測試路線", "測試用路線", "volunteer1")
        
        # 建立每日任務（分配給 volunteer1）
        task_id = db_manager.create_daily_task("2024-01-01", route_id, "volunteer1")
        
        # 儲存測試用 ID
        cls.route_id = route_id
        cls.task_id = task_id
        cls.assigned_user = "volunteer1"
        cls.unauthorized_user = "volunteer2"

    def _create_test_image(self):
        """建立測試用圖片"""
        img = Image.new('RGB', (100, 100), color='red')
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        return buffer

    def test_1_authorized_user_can_upload(self):
        """測試：被分配的志工可以上傳照片"""
        print("\n測試 1: 被分配的志工應該可以上傳照片")
        
        test_image = self._create_test_image()
        
        try:
            photo_path = utils.save_proof_photo(
                test_image, 
                self.task_id, 
                current_user=self.assigned_user
            )
            
            self.assertIsNotNone(photo_path, "應該成功儲存照片並返回路徑")
            self.assertTrue(os.path.exists(photo_path), f"照片檔案應該存在：{photo_path}")
            print(f"✅ 成功：被分配的志工 '{self.assigned_user}' 成功上傳照片到 {photo_path}")
            
        except Exception as e:
            self.fail(f"被分配的志工上傳照片時不應該拋出例外：{e}")

    def test_2_unauthorized_user_cannot_upload(self):
        """測試：未被分配的志工不能上傳照片"""
        print("\n測試 2: 未被分配的志工不應該能上傳照片")
        
        test_image = self._create_test_image()
        
        with self.assertRaises(PermissionError) as context:
            utils.save_proof_photo(
                test_image, 
                self.task_id, 
                current_user=self.unauthorized_user
            )
        
        error_message = str(context.exception)
        self.assertIn("權限不足", error_message, "應該返回權限不足的錯誤訊息")
        print(f"✅ 成功：未分配的志工 '{self.unauthorized_user}' 被正確阻止，錯誤訊息：{error_message}")

    def test_3_invalid_task_id(self):
        """測試：不存在的任務 ID 應該返回錯誤"""
        print("\n測試 3: 不存在的任務 ID 應該被拒絕")
        
        test_image = self._create_test_image()
        invalid_task_id = 99999
        
        with self.assertRaises(ValueError) as context:
            utils.save_proof_photo(
                test_image, 
                invalid_task_id, 
                current_user=self.assigned_user
            )
        
        error_message = str(context.exception)
        self.assertIn("不存在", error_message, "應該返回任務不存在的錯誤訊息")
        print(f"✅ 成功：無效的任務 ID {invalid_task_id} 被正確拒絕，錯誤訊息：{error_message}")

    def test_4_backward_compatibility_without_auth(self):
        """測試：向後相容性 - 未提供 current_user 時跳過驗證（用於測試環境）"""
        print("\n測試 4: 向後相容性 - 未提供 current_user 參數時應該跳過驗證")
        
        test_image = self._create_test_image()
        
        try:
            photo_path = utils.save_proof_photo(
                test_image, 
                self.task_id, 
                current_user=None  # 不提供使用者資訊
            )
            
            self.assertIsNotNone(photo_path, "應該成功儲存照片（向後相容模式）")
            print(f"✅ 成功：向後相容模式正常運作，照片儲存到 {photo_path}")
            
        except Exception as e:
            self.fail(f"向後相容模式不應該拋出例外：{e}")

    def test_5_unassigned_task(self):
        """測試：未分配志工的任務應該被拒絕"""
        print("\n測試 5: 未分配志工的任務應該被拒絕")
        
        # 建立一個未分配志工的任務
        unassigned_task_id = db_manager.create_daily_task("2024-01-02", self.route_id, None)
        
        test_image = self._create_test_image()
        
        with self.assertRaises(PermissionError) as context:
            utils.save_proof_photo(
                test_image, 
                unassigned_task_id, 
                current_user=self.assigned_user
            )
        
        error_message = str(context.exception)
        self.assertIn("權限不足", error_message, "應該返回權限不足的錯誤訊息")
        self.assertIn("未分配", error_message, "錯誤訊息應該提到任務未分配")
        print(f"✅ 成功：未分配的任務被正確拒絕，錯誤訊息：{error_message}")


def run_tests():
    """執行測試"""
    print("=" * 80)
    print("開始測試存取控制 (Access Control) 安全性")
    print("=" * 80)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAccessControl)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 80)
    if result.wasSuccessful():
        print("✅ 所有存取控制測試通過！")
    else:
        print("❌ 部分測試失敗，請檢查上方錯誤訊息")
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
