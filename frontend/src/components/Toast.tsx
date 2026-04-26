import React, { useEffect } from "react";
import { Toast as ToastType } from "../types";
import "./Toast.scss";

interface ToastProps {
  toasts: ToastType[];
  removeToast: (id: number) => void;
}

const Toast: React.FC<ToastProps> = ({ toasts, removeToast }) => {
  return (
    <div className="toast-container">
      {toasts.map((t) => (
        <ToastItem key={t.id} toast={t} removeToast={removeToast} />
      ))}
    </div>
  );
};

const ToastItem: React.FC<{
  toast: ToastType;
  removeToast: (id: number) => void;
}> = ({ toast, removeToast }) => {
  useEffect(() => {
    const timer = setTimeout(() => removeToast(toast.id), 3500);
    return () => clearTimeout(timer);
  }, [toast.id, removeToast]);

  return (
    <div className={`toast toast--${toast.type}`}>
      <span className="toast__icon">
        {toast.type === "success" ? "✓" : "✕"}
      </span>
      <span className="toast__message">{toast.message}</span>
      <button className="toast__close" onClick={() => removeToast(toast.id)}>
        ×
      </button>
    </div>
  );
};

export default Toast;
