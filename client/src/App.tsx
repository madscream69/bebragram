import './App.scss'
import {createBrowserRouter, Navigate, RouterProvider} from "react-router-dom";
import Login from "./pages/Login.tsx";
import Register from "./pages/Register.tsx";
import Profile from "./pages/Profile.tsx";
import Feed from "./pages/Feed.tsx";
import Layout from "./components/Layout.tsx";
import NotFound from "./pages/NotFound.tsx";
function App() {

  // return (
  //     <div className="App">
  //         <Routes>
  //             <Route path="/login" element={<Login />} />
  //             <Route path="/register" element={<Register />} />
  //             <Route path="/profile" element={<Profile />} />
  //             <Route path="/feed" element={<Feed />} />
  //             <Route path="/" element={<Profile />} />
  //         </Routes>
  //     </div>
  // )
    const router = createBrowserRouter([
        {
            path:'/',
            element: <Layout/>,
            children:[
                { index: true, element: <Feed /> },
                { path: "old-home", element: <Navigate to={"/"} /> },
                { path: "login", element: <Login /> },
                { path: "register", element: <Register /> },
                { path: "profile", element: <Profile /> },
                { path: "feed", element: <Feed /> },
                // { path: "category/:categoryId", element: <Category /> },
                // { path: "product/:productId", element: <ProductDetails /> },
                { path: "*", element: <NotFound /> },
            ]
        }
    ])
    return <RouterProvider router={router}/>
}

export default App
