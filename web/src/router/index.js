import { createRouter, createWebHistory } from "vue-router";
import AccidentPage from "@/views/AccidentPage.vue";
import ConfigPage from "@/views/ConfigPage.vue";
import DetailsPage from "@/views/DetailsPage.vue";
import ForecastPage from "@/views/ForecastPage.vue";
import HomePage from "@/views/HomePage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomePage,
    },
    {
      path: "/accident",
      name: "accident",
      component: AccidentPage,
    },
    {
      path: "/config",
      name: "config",
      component: ConfigPage,
    },
    {
      path: "/details",
      name: "details",
      component: DetailsPage,
    },
    {
      path: "/forecast",
      name: "forecast",
      component: ForecastPage,
    },
  ],
});

export default router;
