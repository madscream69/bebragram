import './App.scss'
import {Route, Routes} from "react-router-dom";
import Login from "./pages/Login.tsx";
import Register from "./pages/Register.tsx";
import Profile from "./pages/Profile.tsx";
import Feed from "./pages/Feed.tsx";
function App() {

  return (
      <div className="App">
          <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/feed" element={<Feed />} />
              <Route path="/" element={<Feed />} />
          </Routes>
      </div>
  )
}

export default App
