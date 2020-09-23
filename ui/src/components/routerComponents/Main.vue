<template>
  <div id="main-wrap">
    <div id="header">
      <div style="float: left; cursor: pointer;"
        @click="isMenu=!isMenu">
      <img src="/img/icon/menu_icon.png" class="menu" />
      </div>
      <router-link to="/main">Home</router-link>|
      <router-link to="/main/user" v-if="isUser">User</router-link >|
      <router-link to="/main/mypage">Mypage</router-link>
      <div style='float: right;'>
        <a-button type="danger" @click="isLogoutModal = !isLogoutModal">Logout</a-button>
        <a-modal
          v-model:visible="isLogoutModal"
          title="Logout"
          @ok="logoutOk"
        >
        Would you like to log out?
        </a-modal>
      </div>
    </div>
    <div id="content">
      <div id="left" v-if="isMenu">
        <SideVar />
      </div>
      <div id="right">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import SideVar from "@/components/sideComponents/SideVar.vue";

import { apiUrl, requestRaw } from "@/util.js";

export const redirectName = "content";

const main = {
  name: "Main",
  components: {
    SideVar,
  },
  setup() {
    const router = useRouter();
    const store = useStore();
    const isLogoutModal = ref(false);
    const isMenu = ref(false);

    const getUserState = computed(() => {
      return store.getters["login/DATA"];
    });

    const isUser = getUserState.value.userType == 1 ? true : false;

    const logoutOk = async () => {
      await requestRaw(apiUrl + "Login/Logout", {}, "get");

      router.push({
        name: "login",
      });
    };

    return {
      isLogoutModal,
      logoutOk,
      isUser,
      router,
      isMenu,
    };
  },
};
export default main;
</script>

<style lang="scss" scoped>
#main-wrap {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  overflow: auto;
  overflow-x: hidden;

  #header {
    text-align: center;
    padding: 20px;
    background-color: #3432a2;

    a {
      font-weight: bold;
      margin: 10px;
      color: white;
    }
  }
}
#content {
  flex: 1;
  width: 100%;
  display: flex;
  #left {
    width: 300px;
    min-width: 160px;
    height: 100%;
    background-color: #e1dfef;
    background: linear-gradient(135deg, white, #e1dfef);
  }
  #right {
    flex: 1;
    height: 100%;
    width: 100%;
  }
}
</style>
