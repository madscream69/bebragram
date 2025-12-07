import { NavLink } from "react-router-dom";

function Header() {
    return (
        <>
            <h1>Header</h1>
            {/* <a href="http://localhost:5173/about">about</a> */}
            <NavLink to={"/"}>Home</NavLink>
            <NavLink to={"/login"}>Login</NavLink>
            <NavLink to={"/register"}>Register</NavLink>
            <hr />
        </>
    );
}

export default Header;
