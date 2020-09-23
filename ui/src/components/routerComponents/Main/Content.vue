<template>
  <a-modal :visible="previewVisible" :footer="null" @cancel="previewVisible=!previewVisible">
    <img alt="example" style="width: 100%" :src="previewImage" />
  </a-modal>
  <div class="content-card">
    <a-upload
      v-model:fileList="getState.data"
      :action="apiUrl + 'File'"
      :data="{'directoryNo': directoryNo.directoryNo}"
      method="post"
      name="file"
      list-type="picture-card"
      class="avatar-uploader"
      :multiple="true"
      :show-upload-list="true"
      :before-upload="beforeUpload"
      @preview="handlePreview"
      @change="handleChange"
    >
      <img v-if="imageUrl" :src="imageUrl" alt="avatar" />
      <div v-else>
        <loading-outlined v-if="loading" />
        <plus-outlined v-else />
        <div class="ant-upload-text">Upload</div>
      </div>
    </a-upload>
  </div>
</template>
<script>
import { ref, computed } from "vue";
import { useStore } from "vuex";

import { apiUrl, requestRaw } from "@/util.js";
import { PlusOutlined, LoadingOutlined } from "@ant-design/icons-vue";

const getBase64 = async (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
};

const content = {
  name: "Content",
  components: {
    LoadingOutlined,
    PlusOutlined,
  },
  setup() {
    const store = useStore();
    const previewVisible = ref(false);
    const previewImage = ref("");
    const loading = ref(false);
    const imageUrl = ref("");

    const getState = computed(() => {
      return store.getters["file/STATE"];
    });

    const directoryNo = computed(() => {
      return store.getters["sideVar/DIRECTORY"];
    });

    const handlePreview = async (file) => {
      if (!file.url && !file.preview) {
        file.preview = await getBase64(file.originFileObj);
      }
      previewImage.value = file.url || file.preview;
      previewVisible.value = true;
    };

    const handleChange = async (info) => {
      console.log(info, "HC");
      if (info.file.status === "uploading") {
        loading.value = true;
        return;
      }
      if (info.file.status === "done") {
        loading.value = false;
      }
      if (info.file.status === "error") {
        loading.value = false;
      }
      if (info.file.status === "removed") {
        const params = {
          fileNo: info.file.uid,
          directoryNo: info.file.directoryNo,
        };
        await requestRaw(apiUrl + "File", params, "delete");
      }
    };

    const beforeUpload = (file) => {
      const isJpgOrPng =
        file.type === "image/jpeg" || file.type === "image/png";
      if (!isJpgOrPng) {
        alert("You can only upload JPG/PNG file!");
      }

      const isLt2M = file.size / 4096 / 4096 < 2;
      if (!isLt2M) {
        alert("Image must smaller than 2MB!");
      }
      return isJpgOrPng && isLt2M;
    };

    return {
      previewVisible,
      previewImage,
      loading,
      imageUrl,
      apiUrl,
      getState,
      directoryNo,
      handleChange,
      handlePreview,
      beforeUpload,
    };
  },
};

export default content;
</script>
<style>
.content-card {
  margin: 30px;
  border: white;
  min-width: 400px;
}
.avatar-uploader > .ant-upload {
  width: 128px;
  height: 128px;
}
.ant-upload-select-picture-card i {
  font-size: 32px;
  color: #999;
}
.ant-upload-select-picture-card .ant-upload-text {
  margin-top: 8px;
  color: #666;
}
</style>