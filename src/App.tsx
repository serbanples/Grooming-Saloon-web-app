import { Route, Routes } from 'react-router-dom';

import AuthLayout from './_auth/AuthLayout';
import SigninForm from './_auth/forms/SigninForm';
import SignupForm from './_auth/forms/SignupForm';

import './globals.css';

const App = () => {
  return (
    <main className="flex h-screen">
      <Routes>
        {/* public routes */}
        <Route element={<AuthLayout />}>
          <Route path="/sign-in" element={<SigninForm />} />
          <Route path="/sign-up" element={<SignupForm />} />
        </Route>
      </Routes>
    </main>
  )
}

export default App