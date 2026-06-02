import { ShieldAlert } from "lucide-react";

function MaintenancePage() {
  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4 font-sans">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center border border-slate-100">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-amber-100 rounded-full mb-6">
          <ShieldAlert className="w-10 h-10 text-amber-600" />
        </div>
        <h1 className="text-3xl font-bold text-slate-900 mb-4">系統維護中</h1>
        <p className="text-slate-600 text-lg mb-8 leading-relaxed">
          防災教育館預約系統目前進行內容調整與規劃，暫停所有線上服務。
        </p>
        <div className="pt-6 border-t border-slate-100">
          <p className="text-sm text-slate-400">
            造成不便，敬請見諒。
          </p>
        </div>
      </div>
    </div>
  );
}

function App() {
  return <MaintenancePage />;
}

export default App;
