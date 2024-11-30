<template>
  <div class="app-container">
    <header class="header">
      <div class="header-content">
        <h1 class="logo">WeatherData</h1>
        <nav class="nav-links">
          <a @click.prevent="logout" class="nav-link">Deconnexion</a>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 Leborgne Vincent. WeatherData Project.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: "App",
  methods: {
    logout() {
      localStorage.removeItem("token");
      
      this.$router.push("/login");
    },
  },
};
</script>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  background-color: #1f2937;
  color: #fff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-size: 1rem;
}

.nav-link:hover {
  color: #f59e0b;
}

.main-content {
  flex-grow: 1;
  padding: 2rem;
  background-color: #f9fafb;
}

.footer {
  background-color: #1f2937;
  color: #9ca3af;
  padding: 1rem 2rem;
  text-align: center;
}

.footer-content a {
  color: #f59e0b;
  text-decoration: none;
}

.footer-content a:hover {
  color: #d97706;
  text-decoration: underline;
}
</style>
