import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Users, Building2, ArrowLeft, AlertCircle } from "lucide-react";
import { Link, useLocation } from "wouter";
import { Alert, AlertDescription } from "@/components/ui/alert";

export default function BookingEntry() {
  const [, setLocation] = useLocation();

  const handleBookingTypeSelect = (type: "individual" | "group") => {
    if (type === "individual") {
      setLocation("/booking/individual");
    } else {
      setLocation("/booking/group");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted/30">
      <div className="container py-8">
        <Link href="/">
          <Button variant="ghost" className="mb-6">
            <ArrowLeft className="h-4 w-4 mr-2" />
            返回首頁
          </Button>
        </Link>

        <div className="max-w-4xl mx-auto space-y-6">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold tracking-tight">預約參訪</h1>
            <p className="text-muted-foreground">請選擇您的參訪人數類型</p>
          </div>

          {/* 暫停開放提示 */}
          <Alert className="bg-amber-50 border-amber-200">
            <AlertCircle className="h-4 w-4 text-amber-600" />
            <AlertDescription className="text-amber-800">
              <strong>預約功能調整中：</strong>
              <p className="mt-1">因應館內預登內容規劃調整，目前暫停線上預約服務。如需諮詢，請電洽服務專線。造成不便，敬請見諒。</p>
            </AlertDescription>
          </Alert>

          {/* 選擇卡片 (暫停開放) */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* 一般民眾預約 */}
            <Card className="opacity-60 grayscale cursor-not-allowed border-2">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mb-4">
                  <Users className="h-8 w-8 text-gray-400" />
                </div>
                <CardTitle className="text-2xl text-gray-500">一般民眾</CardTitle>
                <CardDescription className="text-lg font-semibold text-gray-400">
                  (暫停開放)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button className="w-full" size="lg" variant="secondary" disabled>
                  暫不開放
                </Button>
              </CardContent>
            </Card>

            {/* 團體預約 */}
            <Card className="opacity-60 grayscale cursor-not-allowed border-2">
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mb-4">
                  <Building2 className="h-8 w-8 text-gray-400" />
                </div>
                <CardTitle className="text-2xl text-gray-500">團體</CardTitle>
                <CardDescription className="text-lg font-semibold text-gray-400">
                  (暫停開放)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button className="w-full" size="lg" variant="secondary" disabled>
                  暫不開放
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* 注意事項 */}
          <Card className="bg-muted/50">
            <CardHeader>
              <CardTitle className="text-lg">預約須知</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground space-y-2">
              <p>
                <strong>1. 預約時間限制：</strong>
              </p>
              <ul className="list-disc list-inside ml-4 space-y-1">
                <li>最早可預約時間為兩周後</li>
                <li>請至少提前3天完成預約</li>
              </ul>

              <p className="mt-3">
                <strong>2. 人數規定：</strong>
              </p>
              <ul className="list-disc list-inside ml-4 space-y-1">
                <li>一般民眾：5~19人（不接待5人以下散客）</li>
                <li>團體：20~60人（超過60人請分批預約）</li>
              </ul>

              <p className="mt-3">
                <strong>3. 預約確認：</strong>
              </p>
              <ul className="list-disc list-inside ml-4 space-y-1">
                <li>預約成功後將收到確認Email與預約編號</li>
                <li>參訪當天請攜帶預約編號報到</li>
              </ul>

              <p className="mt-3">
                <strong>4. 變更與取消：</strong>
              </p>
              <ul className="list-disc list-inside ml-4 space-y-1">
                <li>如需變更或取消，請提前2天聯絡我們</li>
                <li>聯絡電話：089-123456</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
