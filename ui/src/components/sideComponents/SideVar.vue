<template>
  <div class="side-header">
    <img class ="side-header-icon" src="/img/icon/share-off.png" @click="showModal('share')" />
    <img class ="side-header-icon" src="/img/icon/add_icon2.png" @click="showModal('add')" />
    <img class ="side-header-icon" src="/img/icon/setting_i.png" @click="showModal('change')" />
    <img class ="side-header-icon" src="/img/icon/btn-close.png" @click="showModal('delete')" />
  </div>

  <a-modal
    v-model:visible="isAddModal"
    okText="Add"
    :title="!!getCuurentDirectory && 'Add Directory (No.' + getCuurentDirectory.directoryNo + ')'"
    @ok="modalOk('add')"
  >
  <a-input v-model:value="inputName" placeholder="Directory Name" />
  </a-modal>

  <a-modal
    v-model:visible="isChangeModal"
    okText="Change"
    :title="!!getCuurentDirectory && 'Change Directory (No.' + getCuurentDirectory.directoryNo + ')'"
    @ok="modalOk('change')"
  >
  <a-input v-model:value="inputName" placeholder="Directory Name" />
  </a-modal>

  <a-modal
    v-model:visible="isDeleteModal"
    okText="Delete"
    :title="!!getCuurentDirectory && 'Delete Directory (No.' + getCuurentDirectory.directoryNo + ')'"
    @ok="modalOk('delete')"
  >
  Do you want to delete directory? # {{ !!getCuurentDirectory && getCuurentDirectory.directoryNo }}
  </a-modal>

  <a-modal
    v-model:visible="isShareModal"
    okText="Share"
    :title="!!getCuurentDirectory && 'Share Directory (No.' + getCuurentDirectory.directoryNo + ')'"
    @ok="modalOk('share')"
  >
  <a-input v-model:value="inputName" placeholder="User Id" />
  </a-modal>
  
  <ul id="demo">
    <SideVarItem
      class="item"
      v-for="(child, index) in getSideVarState.data"
      :key="index"
      :item="child"
    />
  </ul>
</template>

<script>
import SideVarItem from "@/components/sideComponents/SideVarItem.vue";
import { useStore } from "vuex";
import { ref, computed } from "vue";

import { apiUrl, requestRaw, checkAPIResult } from "@/util.js";

export default {
  name: "SideVar",
  components: {
    SideVarItem,
  },
  setup() {
    const store = useStore();
    const isAddModal = ref(false);
    const isChangeModal = ref(false);
    const isDeleteModal = ref(false);
    const isShareModal = ref(false);
    const inputName = ref("");

    const getUserState = computed(() => {
      return store.getters["login/DATA"];
    });

    const getSideVarState = computed(() => {
      return store.getters["sideVar/STATE"];
    });

    const getCuurentDirectory = computed(() => {
      return store.getters["sideVar/DIRECTORY"];
    });

    const showModal = (type) => {
      if (type == "add") {
        inputName.value = "";
        isAddModal.value = !isAddModal.value;
      } else if (
        type == "change" &&
        !!getCuurentDirectory.value.parentDirectoryNo
      ) {
        inputName.value = getCuurentDirectory.value.directoryName;
        isChangeModal.value = !isChangeModal.value;
      } else if (
        type == "delete" &&
        (!!getCuurentDirectory.value.parentDirectoryNo ||
          getUserState.value.userNo != getCuurentDirectory.value.directoryOwner)
      ) {
        isDeleteModal.value = !isDeleteModal.value;
      } else if (type == "share") {
        inputName.value = "";
        isShareModal.value = !isShareModal.value;
      }
    };

    const modalOk = async (type) => {
      if (type == "share") {
        const params = {
          directoryNo: getCuurentDirectory.value.directoryNo,
          userId: inputName.value,
        };
        await requestRaw(apiUrl + "Directory/Share", params, "post");
        isShareModal.value = false;
      } else {
        const params = {
          directoryNo: getCuurentDirectory.value.directoryNo,
          directoryName: inputName.value,
        };

        const treeData = checkAPIResult(
          await requestRaw(
            apiUrl + "Directory",
            params,
            type == "add" ? "post" : type == "change" ? "put" : "delete"
          )
        );
        if (treeData) {
          store.dispatch("sideVar/SET_DATA", treeData);
        }

        if (type == "add") {
          isAddModal.value = false;
        } else if (type == "change") {
          const params = { directoryNo: treeData[0].directoryNo };

          const fileList = checkAPIResult(
            await requestRaw(apiUrl + "File", params, "get")
          );
          if (fileList) {
            store.dispatch("file/SET_DATA", fileList);
            store.dispatch("sideVar/SET_DIRECTORY", treeData[0]);
          }
          isChangeModal.value = false;
        } else if (type == "delete") {
          isDeleteModal.value = false;
        }
      }
    };

    const getDirectory = async () => {
      const treeData = checkAPIResult(
        await requestRaw(apiUrl + "Directory", {}, "get")
      );
      if (treeData) {
        store.dispatch("sideVar/SET_DATA", treeData);
      }

      const params = { directoryNo: treeData[0].directoryNo };

      const fileList = checkAPIResult(
        await requestRaw(apiUrl + "File", params, "get")
      );
      if (fileList) {
        store.dispatch("file/SET_DATA", fileList);
        store.dispatch("sideVar/SET_DIRECTORY", treeData[0]);
      }
    };

    getDirectory();

    return {
      getSideVarState,
      getCuurentDirectory,
      inputName,
      isAddModal,
      isChangeModal,
      isDeleteModal,
      isShareModal,
      showModal,
      modalOk,
    };
  },
};
</script>

<style lang="scss" scoped>
#demo {
  width: 100%;
  text-align: left;
  margin: 0px;
  padding: 0px;
}

.side-header {
  text-align: right;
  margin: 10px;

  .side-header-icon {
    margin: 0 10px;
    cursor: pointer;
  }
}
</style>
