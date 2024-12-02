<template>
  <div class="container">
    <h1>Bienvenue sur votre Weather Data Dashboard</h1>

    <!-- Sélection de la station -->
    <label for="station">Sélectionnez une station :</label>
    <select id="station" v-model="selectedStation">
      <option v-for="station in stations" :key="station" :value="station">
        {{ station }}
      </option>
    </select>

    <!-- Graphiques -->
    <div class="charts">
      <MaxTemperatureChart :station="selectedStation" />
      <PrecipitationChart :station="selectedStation" />
      <WindSpeedChart :station="selectedStation" />
      <CorrelationChart />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import MaxTemperatureChart from "@/components/graphs/MaxTemperatureChart.vue";
import PrecipitationChart from "@/components/graphs/PrecipitationChart.vue";
import WindSpeedChart from "@/components/graphs/WindSpeedChart.vue";
import CorrelationChart from "@/components/graphs/CorrelationChart.vue";

export default {
  data() {
    return {
      stations: [],
      selectedStation: "",
    };
  },
  components: {
    MaxTemperatureChart,
    PrecipitationChart,
    WindSpeedChart,
    CorrelationChart,
  },
  async created() {
    await this.fetchStations();
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
        }
      } catch (error) {
        console.error("Erreur lors du chargement des stations :", error.response?.data || error.message);
      }
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
.charts {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
