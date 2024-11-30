<template>
    <div class="login-container">
      <div class="login-card">
        <h2 class="login-title">{{ isLoginMode ? 'Login to your account' : 'Create an account' }}</h2>
        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-group">
            <label for="username">Username</label>
            <input v-model="form.username" id="username" type="text" required />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input v-model="form.password" id="password" type="password" required />
          </div>
          <div class="form-group" v-if="!isLoginMode">
            <label for="confirmPassword">Confirm Password</label>
            <input v-model="form.confirmPassword" id="confirmPassword" type="password" required />
          </div>
          <button type="submit" class="submit-button">
            {{ isLoginMode ? 'Login' : 'Register' }}
          </button>
        </form>
        <p class="switch-mode">
          {{ isLoginMode ? "Don't have an account?" : "Already have an account?" }}
          <a href="#" @click.prevent="toggleMode">
            {{ isLoginMode ? 'Register here' : 'Login here' }}
          </a>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        isLoginMode: true,
        form: {
          username: "",
          password: "",
          confirmPassword: "",
        },
      };
    },
    methods: {
      toggleMode() {
        this.isLoginMode = !this.isLoginMode;
      },
      async handleSubmit() {
        try {
          if (this.isLoginMode) {
            // Login API request
            const response = await axios.post("http://127.0.0.1:8000/api/auth/login", {
              username: this.form.username,
              password: this.form.password,
            });
  
            // Stocker le token dans localStorage
            const token = response.data.access_token;
            localStorage.setItem("token", token);
            console.log("Login Success:", response.data);
  
            // Rediriger vers la page principale après connexion
            this.$router.push("/");
          } else {
            // Register API request
            if (this.form.password !== this.form.confirmPassword) {
              alert("Passwords do not match!");
              return;
            }
            const response = await axios.post("http://127.0.0.1:8000/api/auth/register", {
              username: this.form.username,
              password: this.form.password,
            });
  
            console.log("Register Success:", response.data);
            alert("Registered successfully!");
  
            // Après inscription, basculez vers le mode login
            this.toggleMode();
          }
        } catch (error) {
          console.error("Error:", error.response?.data || error.message);
          alert(error.response?.data?.detail || "An error occurred");
        }
      },
    },
  };
  </script>
  
  
  <style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f9fafb;
  }
  
  .login-card {
    background: #fff;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 100%;
  }
  
  .login-title {
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1.5rem;
  }
  
  .login-form {
    display: flex;
    flex-direction: column;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    display: block;
    font-weight: bold;
  }
  
  .form-group input {
    width: 100%;
    padding: 0.5rem;
    font-size: 0.9rem;
    border: 1px solid #d1d5db;
    border-radius: 4px;
  }
  
  .submit-button {
    background-color: #4f46e5;
    color: #fff;
    border: none;
    padding: 0.75rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    margin-top: 1rem;
    text-align: center;
  }
  
  .submit-button:hover {
    background-color: #4338ca;
  }
  
  .switch-mode {
    margin-top: 1rem;
    text-align: center;
    font-size: 0.85rem;
  }
  
  .switch-mode a {
    color: #4f46e5;
    text-decoration: none;
    font-weight: bold;
  }
  
  .switch-mode a:hover {
    text-decoration: underline;
  }
  </style>
  