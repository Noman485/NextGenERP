import { Route, Routes } from 'react-router-dom';

import App from './App';
import AdminApp from './pages/admin/AdminApp';
import AdminLogin from './pages/admin/AdminLogin';

export default function Root() {
  return (
    <Routes>
      <Route path="/admin/login" element={<AdminLogin />} />
      <Route path="/admin/*" element={<AdminApp />} />
      <Route path="*" element={<App />} />
    </Routes>
  );
}
