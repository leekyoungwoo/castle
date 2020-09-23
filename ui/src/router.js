// const dynamicModule = x => () => import(`@/components/${x}.vue`);
import store from "@/store/index";
import { apiUrl, requestRaw, checkAPIResult } from "@/util.js";

const checkAuth = () => {
  return async (from, to, next) => {
    try {
      const respObj = checkAPIResult(
        await requestRaw(apiUrl + "Login/CheckLogin", {}, "post")
      );
      if (respObj) {
        const data = respObj[0];

        if (data.loginResult === 1 && data.userData && data.userData.isEnable) {
          store.dispatch("login/SET_DATA", data);

          return next();
        } else {
          return next("/login");
        }
      }
    } catch (error) {
      console.log(error); // Error: Request is failed
      return next("/login");
    }
  };
};

const dynamicModule = (x) => require(`@/components/routerComponents/${x}.vue`);
const router = (copyRoute, componentArray, module, index) => {
  var add = true;
  for (let i in copyRoute) {
    if (copyRoute[i].name === componentArray[0].toLowerCase()) {
      copyRoute[i].children = router(
        copyRoute[i].children,
        componentArray.slice(1),
        module,
        1
      );
      add = false;
    }
  }

  if (add) {
    var dict = {
      path:
        index === 0
          ? "/" + componentArray[0].toLowerCase()
          : componentArray[0].toLowerCase(),
      name: componentArray[0].toLowerCase(),
      component: module.default,
      beforeEnter:
        componentArray[0].toLowerCase() == "login" ? "" : checkAuth(),
      children: [],
    };
    if (module.redirectName && !!module.redirectName) {
      dict.children.push({
        path: "",
        name: componentArray[0].toLowerCase(),
        redirect: { name: module.redirectName },
      });
    }
    copyRoute.push(dict);
  }
  return copyRoute;
};

let basicRoutes = [
  {
    path: "/",
    redirect: { name: "content" },
  },
];

const req = require.context(
  "@/components/routerComponents",
  true,
  /^(?!.\/index).*.vue$/
);

req.keys().forEach((key) => {
  const component = key.substring(2).replace(".vue", "");
  const componentArray = component.split("/");
  // const module = dynamicModule(component)
  const module = dynamicModule(component);
  // console.log(module)
  basicRoutes = router(basicRoutes, componentArray, module, 0);
});
console.log(basicRoutes);
const routes = basicRoutes;

export default routes;
