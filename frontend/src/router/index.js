import { createWebHistory, createRouter } from "vue-router"
import Map from "@/components/Map.vue"
import Twitter from "@/components/Twitter.vue"

const routes = [
  {
    path: "/",
    redirect:'/map'
  },
  {
    path: "/map",
    name: "map",
    component: Map,
    meta: {
      title: "Project"
    }
  },
  {
    path: "/twitter",
    name: "twitter",
    component: Twitter,
    meta: {
      title: "Project"
    }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;