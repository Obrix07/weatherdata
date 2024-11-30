<template>
    <div class="container">
      <h1>Bienvenue sur votre  Weather Data Dashboard</h1>
  
      <label for="station">Sélectionné une station:</label>
      <select id="station" v-model="selectedStation" @change="fetchTemperatureData">
        <option v-for="station in stations" :key="station" :value="station">
          {{ station }}
        </option>
      </select>
  
      <div v-if="chartData.length > 0">
        <canvas id="temperatureChart"></canvas>
      </div>
      <p v-else>Aucune donnée disponible pour cette station.</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import Chart from "chart.js/auto";
  
  export default {
    data() {
      return {
        stations: [], // Liste des stations
        selectedStation: "", // Station sélectionnée
        chart: null, // Instance du graphique
        chartData: [], // Données pour le graphique
      };
    },
    async created() {
      await this.fetchStations(); // Charger les noms des stations au chargement
    },
    methods: {
      async fetchStations() {
        try {
          const response = await axios.get("http://127.0.0.1:8000/api/data/stations", {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          });
          this.stations = response.data.stations;
          if (this.stations.length > 0) {
            this.selectedStation = this.stations[0];
            this.fetchTemperatureData();
          }
        } catch (error) {
          console.error("Erreur lors du chargement des stations :", error.response?.data || error.message);
        }
      },
      async fetchTemperatureData() {
        try {
          const response = await axios.get("http://127.0.0.1:8000/api/data/max-temperature", {
            params: { station_name: this.selectedStation },
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          });
          this.chartData = response.data;
  
          this.renderChart();
        } catch (error) {
          console.error("Erreur lors du chargement des données :", error.response?.data || error.message);
        }
      },
      renderChart() {
        // Détruire le graphique existant (si présent)
        if (this.chart) {
          this.chart.destroy();
        }
  
        // Préparer les données pour Chart.js
        const labels = this.chartData.map((data) => data.date);
        const data = this.chartData.map((data) => data.max_temperature);
  
        // Créer un nouveau graphique
        const ctx = document.getElementById("temperatureChart").getContext("2d");
        this.chart = new Chart(ctx, {
          type: "line",
          data: {
            labels,
            datasets: [
              {
                label: "Max Temperature",
                data,
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
          },
        });
      },
    },
  };
  </script>
  
  <style>
  .container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
  }
  canvas {
    max-height: 400px;
  }
  </style>
  