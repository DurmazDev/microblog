const config = {
  PROTECTED_ROUTES: [
    "/profile",
    "/create",
    "/chat",
    "/setup-2fa",
  ],
  apiUrl: "http://api.microblog.local:8000/",
  frontendUrl: "http://microblog.local:4173/",
  devMode: true,
};

export default config;
