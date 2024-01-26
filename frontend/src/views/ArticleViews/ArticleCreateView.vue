<template>
  <p>Article Create</p>
  <input
    class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-4 focus:outline-none focus:border-primary-600"
    placeholder="Article Title"
    @input="this.title = $event.target.value"
  />
  <QuillEditor
    style="min-height: 300px"
    ref="editorRef"
  />
  <button
    class="float-right text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 m-2 focus:outline-none"
    @click="submitArticle()"
  >
    Submit Article
  </button>
</template>
<script>
  import { QuillEditor } from "@vueup/vue-quill";
  import config from "@/config";
  import "@vueup/vue-quill/dist/vue-quill.snow.css";
  import { useToast } from "vue-toastify";

  export default {
    name: "CreateArticleView",
    components: {
      QuillEditor,
    },
    data() {
      return {
        title: "",
      };
    },
    methods: {
      getEditor() {
        return this.$refs.editorRef.getHTML();
      },
      submitArticle() {
        this.axios({
          method: "post",
          url: "/post",
          data: JSON.stringify({
            title: this.title,
            content: this.getEditor(),
          }),
        })
          .then((response) => {
            this.$router.push({
              name: "articledetail",
              params: {
                articleUrl: response.data.url?.replace(
                  config.frontendUrl + "post/",
                  ""
                ),
              },
            });
          })
          .catch(() => {
            useToast().error("An error occurred. Please try again later.");
          });
      },
    },
  };
</script>
