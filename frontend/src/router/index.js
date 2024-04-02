import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/AuthViews/LoginView.vue";
import RegisterView from "@/views/AuthViews/RegisterView.vue";
import ProfileView from "@/views/ProfileView.vue";
import UserProfileView from "@/views/UserProfileView.vue";
import AboutView from "@/views/AboutView.vue";
import ArticleDetailView from "@/views/ArticleViews/ArticleDetailView.vue";
import ArticleCreateView from "@/views/ArticleViews/ArticleCreateView.vue";
import ChatView from "@/views/ChatView.vue";
import NotFoundView from "@/views/NotFoundView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/post/:articleUrl",
      name: "articledetail",
      component: ArticleDetailView,
    },
    {
      path: "/create",
      name: "articlecreate",
      component: ArticleCreateView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },
    {
      path: "/profile",
      name: "profile",
      component: ProfileView,
    },
    {
      path: "/profile/:userID",
      name: "user-profile",
      component: UserProfileView,
    },
    {
      path: "/about",
      name: "about",
      component: AboutView,
    },
    {
      path: "/chat",
      name: "chat",
      component: ChatView,
    },
    {
      path: "/:catchAll(.*)*",
      name: "notfound",
      component: NotFoundView,
    },
  ],
});

export default router;
