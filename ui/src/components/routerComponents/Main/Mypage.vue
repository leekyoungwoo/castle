--<template>
  <div class="mypage-content-area">
    <div class="mypage-content-header">
    Profile
      <div style='float: right;'>
        <a-button type="danger" @click="isDeleteModal = !isDeleteModal">Close my account</a-button>
        <a-modal
          v-model:visible="isDeleteModal"
          title="Close my account"
          @ok="deleteOk"
        >
        Do you want to withdraw from membership?
        </a-modal>
      </div>
    </div>
    <div class="mypage-content-input">
      <div class="mypage-content-input-title">
        Name
      </div>
      <input class="input-style" v-on:input="onBind('name', $event)" v-bind:value="user.name" placeholder="User Name" />
    </div>

    <div class="mypage-content-input">
      <div class="mypage-content-input-title">
        ID
      </div>
      <input class="input-style" v-on:input="onBind('id', $event)" v-bind:value="user.id" placeholder="User Id" />
    </div>

    <div class="mypage-content-input">
      <div class="mypage-content-input-title">
        Email
      </div>
      <input class="input-style" v-on:input="onBind('email', $event)" v-bind:value="user.email" placeholder="User Email" />
    </div>

    <div class="mypage-content-input">
      <div class="mypage-content-input-title">
        Contact
      </div>
      <input class="input-style" v-on:input="onBind('phone', $event)" v-bind:value="user.phone" placeholder="User Phone" />
    </div>
    <div>
      <a-button type="primary" :disabled="changed" @click="onClick()">Save</a-button>
      {{ message }}
    </div>
  </div>
</template>
<script>
import { ref, watch, reactive, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

import { apiUrl, requestRaw } from "@/util.js";

const mypage = {
  name: "Mypage",
  setup() {
    const store = useStore();
    const router = useRouter();
    const changed = ref(true);
    const message = ref("");
    const isDeleteModal = ref(false);
    const getUserData = computed(() => {
      return store.getters["login/STATE"];
    });

    const user = reactive({
      name: getUserData.value.data.userName || "",
      id: getUserData.value.data.userId || "",
      email: getUserData.value.data.userEmail || "",
      phone: getUserData.value.data.userPhone || "",
    });

    let params = {};

    const onBind = (type, e) => {
      user[type] = e.target.value;
      console.log(user[type]);
    };

    watch(user, (value) => {
      if (value.name != getUserData.value.data.userName) {
        changed.value = false;
      } else if (value.id != getUserData.value.data.userId) {
        changed.value = false;
      } else if (value.email != (getUserData.value.data.userEmail || "")) {
        changed.value = false;
      } else if (value.phone != (getUserData.value.data.userPhone || "")) {
        changed.value = false;
      } else {
        changed.value = true;
      }
    });

    const onClick = async () => {
      if (user.name != getUserData.value.data.userName) {
        params["userName"] = user.name;
      }
      if (user.id != getUserData.value.data.userId) {
        params["userId"] = user.id;
      }
      if (user.email != (getUserData.value.data.userEmail || "")) {
        params["userEmail"] = user.email;
      }
      if (user.phone != (getUserData.value.data.userPhone || "")) {
        params["userPhone"] = user.phone;
      }

      const respObj = await requestRaw(apiUrl + "User/Edit", params, "post");

      if (respObj) {
        message.value = "저장되었습니다";
      } else {
        message.value = "내정보 수정 실패";
        user.name = getUserData.value.data.userName || "";
        user.id = getUserData.value.data.userId || "";
        user.email = getUserData.value.data.userEmail || "";
        user.phone = getUserData.value.data.userPhone || "";
      }
    };

    const deleteOk = async () => {
      const respObj = await requestRaw(apiUrl + "User/Edit", {}, "delete");

      if (respObj) {
        router.push({
          name: "login",
        });
      } else {
        message.value = "내정보 수정 실패";
        user.name = getUserData.value.data.userName || "";
        user.id = getUserData.value.data.userId || "";
        user.email = getUserData.value.data.userEmail || "";
        user.phone = getUserData.value.data.userPhone || "";
      }
    };

    return {
      user,
      changed,
      message,
      isDeleteModal,
      onBind,
      onClick,
      deleteOk,
    };
  },
};
export default mypage;
</script>

<style lang="scss" scoped>
.mypage-content-area {
  position: relative;
  min-width: 300px;
  min-height: 300px;
  margin: 100px;
  text-align: left;
  .mypage-content-header {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 30px;
  }
  .mypage-content-input {
    font-size: 15px;
    margin-bottom: 20px;

    .mypage-content-input-title {
      margin-bottom: 10px;
    }
    .input-style {
      width: 200px;
    }
  }
}
</style>