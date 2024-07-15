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
  <Multiselect
    v-model="value"
    mode="tags"
    :close-on-select="false"
    :options="options"
    :searchable="true"
    placeholder="Select tags"
  />
  <div class="flex">
    <input
      class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-4 focus:outline-none focus:border-primary-600"
      placeholder="or Create new tag here"
      @input="this.newTag = $event.target.value"
    />
    <button
      class="text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-4 lg:px-5 focus:outline-none"
      @click="addTag()"
    >
      Add Tag
    </button>
  </div>
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
  import Multiselect from "@vueform/multiselect";
  import "@vueform/multiselect/themes/default.css";

  export default {
    name: "CreateArticleView",
    components: {
      QuillEditor,
      Multiselect,
    },
    data() {
      return {
        title: "",
        value: [],
        options: {},
        newTag: null,
      };
    },
    mounted() {
      this.getTags();
    },
    methods: {
      getTags() {
        this.axios({
          method: "get",
          url: "/tag",
        })
          .then((response) => {
            for (let i = 0; i < response.data.length; i++) {
              this.options[response.data[i].id] = response.data[i].name;
            }
          })
          .catch(() => {
            useToast().error("An error occurred. Please try again later.");
          });
      },
      addTag() {
        this.axios({
          method: "post",
          url: "/tag",
          data: JSON.stringify({
            name: this.newTag,
          }),
        })
          .then((response) => {
            this.options[response.data.id] = response.data.name;
            this.value.push(response.data.id);
          })
          .catch((err) => {
            if (err.response.status === 409) {
              useToast().error("Tag already exists.");
              this.value.push(err.response.data.id);
              return;
            }
            useToast().error("An error occurred. Please try again later.");
          });
      },
      getEditor() {
        return this.$refs.editorRef.getHTML();
      },
      submitArticle() {
        let data = {
          title: this.title,
          content: this.getEditor(),
        };
        if (this.value.length > 0) {
          data["tags"] = this.value;
        }
        this.axios({
          method: "post",
          url: "/post",
          data: JSON.stringify(data),
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
