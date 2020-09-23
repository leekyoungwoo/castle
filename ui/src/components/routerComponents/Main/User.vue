<template>
  <div class="user-header">
    <a-button
      class="user-header-btn"
      size="large"
      type="primary"
      @click="isModalFunc('add', {})"
      >Add
    </a-button>
  </div>
  <a-modal
      v-model:visible="isModal"
      okText="Ok"
      :title="modalType === 'put' ? (!!selectedUser.userNo && 'Edit User (No.' + selectedUser.userNo + ')') : modalType === 'add' ? 'Add User' : 'Delete User'"
      @ok="modalOk(modalType)"
    >
    <div v-if="modalType === 'delete'">
      Are you sure you want to delete?
    </div>
    <div v-else>
      <div class="input-text">
        Name
      </div>
      <input class="input-style" v-on:input="onBind('userName', $event)" v-bind:value="selectedUser.userName" placeholder="User Name" />
      <div class="input-text">
        ID
      </div>
      <input class="input-style" v-on:input="onBind('userId', $event)" v-bind:value="selectedUser.userId" placeholder="User Id" />
      <div class="input-text">
        Email
      </div>
      <input class="input-style" v-on:input="onBind('userEmail', $event)" v-bind:value="selectedUser.userEmail" placeholder="User Email" />
      <div class="input-text">
        PassWord
      </div>
      <input class="input-style" v-on:input="onBind('userPasswd', $event)" v-bind:value="selectedUser.userPasswd" placeholder="User Passwd" type="password" />
    </div>
  </a-modal>
  <div class="user-wrap">
    <a-table :columns="columns" :data-source="getUserState.data">
      <template v-slot:userType="{ text: type }">
        <span>
          <a-tag
            :key="type"
            :color="type === 1 ? 'geekblue' : 'green'"
          >
            {{ type === 1 ? "관리자" : "사용자"}}
          </a-tag>
        </span>
      </template>
      <template v-slot:action="{ record }">
        <span>
          <a @click="isModalFunc('put', record)">Edit</a> 
          <a-divider type="vertical"  v-if="record.userType===2"/>
          <a @click="isModalFunc('delete', record)" v-if="record.userType===2">Delete</a>
        </span>
      </template>
    </a-table>
  </div>
</template>
<script>
import { apiUrl, requestRaw, checkAPIResult } from "@/util.js";
import { useStore } from "vuex";
import { ref, computed, reactive } from "vue";

const setUserList = async (store) => {
  const userList = checkAPIResult(await requestRaw(apiUrl + "User", {}, "get"));

  if (userList) {
    store.dispatch("user/SET_DATA", userList);
  }
};

const user = {
  name: "User",
  components: {},
  setup() {
    const store = useStore();
    setUserList(store);
    const getUserState = computed(() => {
      return store.getters["user/STATE"];
    });

    const isModal = ref(false);
    const selectedUser = reactive({});
    const modalType = ref("");

    const isModalFunc = (type, info) => {
      isModal.value = !isModal.value;
      selectedUser.userNo = info.userNo;
      selectedUser.userName = info.userName;
      selectedUser.userEmail = info.userEmail;
      selectedUser.userId = info.userId;
      selectedUser.userType = info.userType;
      selectedUser.userPasswd = "";
      if (type == "add") {
        modalType.value = "add";
      } else if (type == "put") {
        modalType.value = "put";
      } else if (type == "delete") {
        modalType.value = "delete";
      }
    };

    const onBind = (type, e) => {
      selectedUser[type] = e.target.value;
    };

    const modalOk = async (type) => {
      const params = {
        userNo: selectedUser.userNo,
      };

      if (type !== "delete") {
        params["userName"] = selectedUser.userName;
        params["userEmail"] = selectedUser.userEmail;
        params["userId"] = selectedUser.userId;
        if (selectedUser.userPasswd) {
          params["userPasswd"] = selectedUser.userPasswd;
        }
        if (type === "put") {
          const userData = checkAPIResult(
            await requestRaw(apiUrl + "User", params, "put")
          );
          store.dispatch("user/SET_DATA", userData);
        } else if (type === "add") {
          const userData = checkAPIResult(
            await requestRaw(apiUrl + "User", params, "post")
          );
          store.dispatch("user/SET_DATA", userData);
        }
      } else if (type === "delete") {
        const userData = checkAPIResult(
          await requestRaw(apiUrl + "User", params, "delete")
        );
        store.dispatch("user/SET_DATA", userData);
      }

      isModal.value = !isModal.value;
    };

    const columns = [
      {
        title: "No",
        dataIndex: "userNo",
        key: "userNo",
        width: "20px",
      },
      {
        title: "ID",
        dataIndex: "userId",
        key: "userId",
        width: "20px",
      },
      {
        title: "Name",
        dataIndex: "userName",
        key: "userName",
        width: "20px",
      },
      {
        title: "Email",
        dataIndex: "userEmail",
        key: "userEmail",
        width: "20px",
      },
      {
        title: "Type",
        key: "userType",
        dataIndex: "userType",
        width: "20px",
        slots: { customRender: "userType" },
      },
      {
        title: "Action",
        key: "action",
        width: "20px",
        slots: { customRender: "action" },
      },
    ];

    return {
      getUserState,
      columns,
      isModal,
      selectedUser,
      modalType,
      isModalFunc,
      onBind,
      modalOk,
    };
  },
};

export default user;
</script>

<style lang="scss" scoped>
.user-wrap {
  margin: 30px;
  border: white;
  min-width: 400px;
}
.input-style {
  width: 400px;
  padding: 5px;
}
.input-text {
  margin: 10px 0;
  font-weight: bold;
}
.user-header {
  text-align: right;
  margin: 10px;

  .user-header-btn {
    margin: 0 10px;
  }
}
</style>