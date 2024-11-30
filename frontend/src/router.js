import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "./views/LoginPage.vue";
import HomePage from "./views/HomePage.vue";
import axios from "axios";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/login", name: "Login", component: LoginPage },
    {
      path: "/",
      name: "Home",
      component: HomePage,
      beforeEnter: async (to, from, next) => {
        // Récupérez le token du localStorage
        const storedToken = localStorage.getItem("token");

        // Si aucun token n'est trouvé, redirigez vers /login
        if (!storedToken) {
          return next("/login");
        }

        const token = storedToken;

        try {
          // Vérifiez la validité du token en appelant l'API de validation
          await axios.get("http://127.0.0.1:8000/api/auth/validate-token", {
            headers: { Authorization: `Bearer ${token}` },
          });

          // Si le token est valide, laissez l'accès
          next();
        } catch (error) {
          console.error("Token invalide ou expiré :", error.response?.data || error.message);
          // Si le token est invalide ou expiré, redirigez vers /login
          localStorage.removeItem("token"); // Nettoyez le token invalide du localStorage
          next("/login");
        }
      },
    },
  ],
});

export default router;
