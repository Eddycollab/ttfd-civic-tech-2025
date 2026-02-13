"""
測試存取控制 (Access Control) 安全性
驗證 save_proof_photo() 函數的權限檢查是否正確運作
"""
import sys
import os
import pytest
import tempfile
from io import BytesIO
from PIL import Image

# 將專案根目錄加入 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db_manager
import utils


@pytest.fixture(scope="module")
def setup_test_db():
    """測試前準備：建立測試資料庫"""
    # 使用臨時資料庫
    original_db = db_manager.DB_NAME
    test_db = "test_access_control.db"
    db_manager.DB_NAME = test_db
    
    # 初始化資料庫
    db_manager.init_db()
    
    # 建立測試資料
    route_id = db_manager.create_delivery_route("測試路線", "測試用路線", "volunteer1")
    task_id = db_manager.create_daily_task("2024-01-01", route_id, "volunteer1")
    
    # 返回測試數據
    test_data = {
        'route_id': route_id,
        'task_id': task_id,
        'assigned_user': 'volunteer1',
        'unauthorized_user': 'volunteer2',
        'original_db': original_db,
        'test_db': test_db
    }
    
    yield test_data
    
    # 清理：刪除測試資料庫
    db_manager.DB_NAME = original_db
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # 清理測試產生的照片
    test_upload_dir = "uploads/delivery_proofs"
    if os.path.exists(test_upload_dir):
        import shutil
        shutil.rmtree(test_upload_dir)


@pytest.fixture
def test_image():
    """建立測試用圖片"""
    img = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer


def test_authorized_user_can_upload(setup_test_db, test_image):
    """測試：被分配的志工可以上傳照片"""
    print("\n測試: 被分配的志工應該可以上傳照片")
    
    photo_path = utils.save_proof_photo(
        test_image, 
        setup_test_db['task_id'], 
        current_user=setup_test_db['assigned_user']
    )
    
    assert photo_path is not None, "應該成功儲存照片並返回路徑"
    assert os.path.exists(photo_path), f"照片檔案應該存在：{photo_path}"
    print(f"✅ 成功：被分配的志工 '{setup_test_db['assigned_user']}' 成功上傳照片到 {photo_path}")


def test_unauthorized_user_cannot_upload(setup_test_db, test_image):
    """測試：未被分配的志工不能上傳照片"""
    print("\n測試: 未被分配的志工不應該能上傳照片")
    
    with pytest.raises(PermissionError) as exc_info:
        utils.save_proof_photo(
            test_image, 
            setup_test_db['task_id'], 
            current_user=setup_test_db['unauthorized_user']
        )
    
    error_message = str(exc_info.value)
    assert "權限不足" in error_message, "應該返回權限不足的錯誤訊息"
    print(f"✅ 成功：未分配的志工 '{setup_test_db['unauthorized_user']}' 被正確阻止，錯誤訊息：{error_message}")


def test_invalid_task_id(setup_test_db, test_image):
    """測試：不存在的任務 ID 應該返回錯誤"""
    print("\n測試: 不存在的任務 ID 應該被拒絕")
    
    invalid_task_id = 99999
    
    with pytest.raises(ValueError) as exc_info:
        utils.save_proof_photo(
            test_image, 
            invalid_task_id, 
            current_user=setup_test_db['assigned_user']
        )
    
    error_message = str(exc_info.value)
    assert "不存在" in error_message, "應該返回任務不存在的錯誤訊息"
    print(f"✅ 成功：無效的任務 ID {invalid_task_id} 被正確拒絕，錯誤訊息：{error_message}")


def test_backward_compatibility_without_auth(setup_test_db, test_image):
    """測試：向後相容性 - 未提供 current_user 時跳過驗證（用於測試環境）"""
    print("\n測試: 向後相容性 - 未提供 current_user 參數時應該跳過驗證")
    
    photo_path = utils.save_proof_photo(
        test_image, 
        setup_test_db['task_id'], 
        current_user=None  # 不提供使用者資訊
    )
    
    assert photo_path is not None, "應該成功儲存照片（向後相容模式）"
    print(f"✅ 成功：向後相容模式正常運作，照片儲存到 {photo_path}")


def test_unassigned_task(setup_test_db, test_image):
    """測試：未分配志工的任務應該被拒絕"""
    print("\n測試: 未分配志工的任務應該被拒絕")
    
    # 建立一個未分配志工的任務
    unassigned_task_id = db_manager.create_daily_task(
        "2024-01-02", 
        setup_test_db['route_id'], 
        None
    )
    
    with pytest.raises(PermissionError) as exc_info:
        utils.save_proof_photo(
            test_image, 
            unassigned_task_id, 
            current_user=setup_test_db['assigned_user']
        )
    
    error_message = str(exc_info.value)
    assert "權限不足" in error_message, "應該返回權限不足的錯誤訊息"
    assert "未分配" in error_message, "錯誤訊息應該提到任務未分配"
    print(f"✅ 成功：未分配的任務被正確拒絕，錯誤訊息：{error_message}")
