import { createRouter, createWebHistory } from "vue-router";
import { createApp } from "vue";
import * as antd from "ant-design-vue";

// import { routes } from '.';
import routes from "@/router";
import App from "./App.vue";
import store from "@/store";

import "ant-design-vue/dist/antd.css";

const routerHistory = createWebHistory();
const router = createRouter({
  history: routerHistory,
  routes: routes,
});

const app = createApp(App);
app.use(router);
app.use(store);
app.use(antd);
app.mount("#app");
