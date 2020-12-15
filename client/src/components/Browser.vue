<template>
  <div class="container">
    <div class="row">
      <!-- <v-file-input
        color="deep-purple accent-4"
        counter
        label="File input"
        multiple
        placeholder="Select your files"
        prepend-icon="mdi-paperclip"
        outlined
        :show-size="1000"
      >
        <template v-slot:selection="{ index, text }">
          <v-chip
            v-if="index < 2"
            color="deep-purple accent-4"
            dark
            label
            small
          >
            {{ text }}
          </v-chip>

          <span
            v-else-if="index === 2"
            class="overline grey--text text--darken-3 mx-2"
          >
            +{{ files.length - 2 }} File(s)
          </span>
        </template>
      </v-file-input> -->
      <input type="file" id="files" ref="files" multiple v-on:change="handleFileUpload()"/> 
    </div>
    <div class="row justify-content-end">
      <button class="btn btn-primary" @click="submitFile()">Submit</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Browser",
  data: () => ({
    files: [],
  }),
  methods: {
    submitFile() {
      const formData = new FormData();
      formData.append("file", this.files);
      formData.append("k", 1);
      this.progress = true;
      axios
        .post("http://127.0.0.1:8082/query", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log("Respuesta local");
          console.log(res);
        })
        .catch((e) => {
          console.log(e);
        });
    },
    handleFileUpload() {
      this.files = this.$refs.files[0];
    },
  },
};
</script>

<style></style>
