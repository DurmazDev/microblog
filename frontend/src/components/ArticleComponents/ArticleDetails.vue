<template>
  <section class="bg-white">
    <div class="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6">
      <div class="mx-auto max-w-screen-sm text-center">
        <h1
          class="mb-4 text-2xl tracking-tight font-extrabold lg:text-4xl text-primary-600"
        >
          {{ article.title }}
        </h1>
        <div
          class="mb-4 text-left"
          v-html="renderHTML(article.content)"
        ></div>
        <div class="flex justify-center">
          <TagButton
            :v-if="article.tags"
            v-for="(tag, index) in article.tags"
            :key="index"
            :tag="tag.name"
          />
        </div>
        <p class="mb-4 text-lg font-light text-gray-500">
          Creator of this content: {{ article.author?.name }}
        </p>
        <p class="mb-4 text-lg font-light text-gray-500">
          Publis Date: {{ new Date(article.created_at).toUTCString() }}
        </p>
      </div>
    </div>
    <div class="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6">
      <div class="mx-auto w-1/6 text-center">
        <div class="grid grid-cols-2 gap-2">
          <div class="col-span-2">
            <p>Total vote point now: {{ article.vote }}</p>
          </div>
          <button
            :class="`p-6 rounded-lg border border-gray-200 shadow-md ${
              article.author?.vote === 1 ? 'bg-green-400' : 'bg-white'
            }`"
            @click="
              article.author?.vote === 1 ? voteEvent('none') : voteEvent('up')
            "
          >
            <div class="flex justify-between items-center mb-5 text-gray-500">
              <div>
                <svg
                  fill="#000000"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M12.781 2.375c-.381-.475-1.181-.475-1.562 0l-8 10A1.001 1.001 0 0 0 4 14h4v7a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-7h4a1.001 1.001 0 0 0 .781-1.625l-8-10zM15 12h-1v8h-4v-8H6.081L12 4.601 17.919 12H15z"
                  />
                </svg>
                <span class="text-sm mb-4">Up Vote</span>
              </div>
            </div>
          </button>
          <button
            :class="`p-6 rounded-lg border border-gray-200 shadow-md ${
              article.author?.vote === -1 ? 'bg-red-400' : 'bg-white'
            }`"
            @click="
              article.author?.vote === -1
                ? voteEvent('none')
                : voteEvent('down')
            "
          >
            <div class="flex justify-between items-center mb-5 text-gray-500">
              <div>
                <svg
                  fill="#000000"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M20.901 10.566A1.001 1.001 0 0 0 20 10h-4V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v7H4a1.001 1.001 0 0 0-.781 1.625l8 10a1 1 0 0 0 1.562 0l8-10c.24-.301.286-.712.12-1.059zM12 19.399 6.081 12H10V4h4v8h3.919L12 19.399z"
                  />
                </svg>
                <span class="text-sm mb-4">Down Vote</span>
              </div>
            </div>
          </button>
        </div>
        <p v-if="article.author?.vote">
          You have already voted, your choice has been painted.
        </p>
      </div>
    </div>
    <div class="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6">
      <div class="mx-auto max-w-screen-sm text-center">
        <h1
          class="mb-4 text-2xl tracking-tight font-extrabold lg:text-4xl text-primary-600"
        >
          Comments
        </h1>
        <div class="grid grid-cols-1 gap-4">
          <div
            v-for="(comment, index) in article.comments"
            :key="index"
            class="p-6 bg-white rounded-lg border border-gray-200 shadow-md"
          >
            <div class="flex justify-between items-center mb-5 text-gray-500">
              <span class="text-sm mb-4">
                <!-- INFO(ahmet): If there is an Invalid Date error, the error is in the backend.  -->
                {{ new Date(comment.created_at).toUTCString() }}
              </span>
              <span class="text-sm mb-4">
                {{ comment.author.name }}
              </span>
            </div>
            <p class="mb-5 font-light text-gray-500">{{ comment.content }}</p>
            <div v-if="this.$store.getters.isAuthenticated">
              <button
                v-if="
                  this.$store.getters.currentUser?.id === comment.author.id &&
                  comment.id !== undefined
                "
                @click="deleteComment(comment.id)"
                class="flex"
              >
                <svg
                  fill="#000000"
                  height="20px"
                  width="20px"
                  version="1.1"
                  id="Layer_1"
                  viewBox="0 0 354.319 354.319"
                  xml:space="preserve"
                >
                  <path
                    id="XMLID_2_"
                    d="M293.765,125.461l-41.574-17.221l17.221-41.574c3.17-7.654-0.464-16.428-8.118-19.599L150.428,1.146
          C142.775-2.024,134,1.61,130.83,9.264l-17.221,41.574L72.035,33.617c-7.654-3.17-16.428,0.464-19.599,8.118
          c-3.17,7.654,0.464,16.428,8.118,19.599l55.433,22.961l96.628,40.024H87.16c-8.284,0-15,6.716-15,15v200c0,8.284,6.716,15,15,15h180
          c8.284,0,15-6.716,15-15V153.126l0.125,0.052c1.877,0.777,3.821,1.146,5.734,1.146c5.886,0,11.472-3.487,13.864-9.264
          C305.053,137.406,301.419,128.631,293.765,125.461z M141.326,62.318l11.48-27.716l83.148,34.441l-11.48,27.716L182.9,79.539
          L141.326,62.318z"
                  />
                </svg>
                Delete Comment
              </button>
            </div>
          </div>
          <div v-if="this.$store.getters.isAuthenticated">
            <p class="mt-6 text-left">Create Comment:</p>
            <textarea
              class="w-full border border-gray-300 rounded-lg px-3 py-2 mb-4 focus:outline-none focus:border-primary-600"
              placeholder="Comment"
              ref="commentTextAreaRef"
            ></textarea>
            <button
              class="float-right text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 m-2 focus:outline-none"
              @click="submitComment()"
            >
              Submit Comment
            </button>
          </div>
          <div v-else>You must be logged in to post a comment.</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
  import { useToast } from "vue-toastify";
  import TagButton from "../TagButtonComponent.vue";

  export default {
    name: "ArticleDetailView",
    components: {
      TagButton,
    },
    props: {
      article: {
        type: Object,
        required: true,
      },
    },
    methods: {
      renderHTML(htmlString) {
        return `<div> ${htmlString} </div>`;
      },
      submitComment() {
        this.axios({
          method: "post",
          url: "/comment",
          data: JSON.stringify({
            post_id: this.article.id,
            content: this.$refs.commentTextAreaRef.value,
          }),
        })
          .then((response) => {
            if (response.status !== 201) {
              useToast().error("An error occurred while creating comment.");
              return;
            }
            this.$emit("update-comment", {
              id: response.data.comment_id,
              content: this.$refs.commentTextAreaRef.value,
              author: {
                id: this.$store.getters.currentUser?.id,
                name: this.$store.getters.currentUser?.name,
              },
              created_at: new Date().toUTCString(),
            });
            this.$refs.commentTextAreaRef.value = "";
            useToast().success("Comment created successfully.");
          })
          .catch(() => {
            useToast().error("An error occurred while creating comment.");
          });
      },
      deleteComment(commentId) {
        this.axios({
          method: "delete",
          url: "/comment/" + commentId,
        })
          .then((response) => {
            if (response.status !== 204) {
              useToast().error("An error occurred while deleting comment.");
              return;
            }
            this.$emit("delete-comment", commentId);
            useToast().success("Comment deleted successfully.");
          })
          .catch(() => {
            useToast().error("An error occurred while deleting comment.");
          });
      },
      voteEvent(type) {
        if (!this.$store.getters.isAuthenticated) {
          useToast().error("You must be logged in to vote.");
          return;
        }
        this.axios({
          method: "post",
          url: "vote",
          data: JSON.stringify({
            post_id: this.article.id,
            vote_value: type === "up" ? 1 : type === "down" ? -1 : 0,
          }),
        })
          .then((response) => {
            if (response.status == 201) {
              let voteChange = 0;

              if (type === "up") {
                voteChange = 1;
              } else if (type === "down") {
                voteChange = -1;
              }

              this.$emit("update-vote", {
                postId: this.article.id,
                voteChange: voteChange,
              });

              useToast().success(response.data.message);
              return;
            }
          })
          .catch((err) => {
            if (err.response.status === 401)
              useToast().error("You must be logged in to vote.");
            else
              useToast().error(
                "An error occurred while voting. Please try again later."
              );
          });
      },
    },
  };
</script>
