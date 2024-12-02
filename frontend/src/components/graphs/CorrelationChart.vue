<template>
    <div>
      <h2>Corrélation entre altitude et température moyenne</h2>
      <p v-if="correlation === null">Chargement de la corrélation...</p>
      <p v-else>
        La corrélation entre l'altitude et la température moyenne est :
        <strong>{{ correlation }}</strong>.
      </p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        correlation: null,
      };
    },
    async mounted() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/data/correlation-altitude-temperature",
          {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          }
        );
        this.correlation = response.data.correlation;
      } catch (error) {
        console.error("Erreur lors de la récupération de la corrélation :", error.response?.data || error.message);
      }
    },
  };
  </script>
  
  <style>
  /* Ajoutez des styles si nécessaire */
  </style>
  