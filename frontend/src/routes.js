import UserProfile from "views/UserProfile.js";

const dashboardRoutes = [
    {
        path: "/user",
        name: "App ID",
        icon: "nc-icon nc-circle-09",
        component: UserProfile,
        layout: "/admin",
    }
];

export default dashboardRoutes;
