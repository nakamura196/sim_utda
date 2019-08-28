<template>
  <div class="wrapper">
    <parallax
      class="section page-header header-filter"
      :style="headerStyle"
    ></parallax>
    <div class="main main-raised">
      <div class="section text-center">
        <div class="container">
          <form class="contact-form">
            <div class="md-layout">
              <div class="md-layout-item md-size-66 mx-auto">
                <div class="md-field md-theme-default">
                  <input
                    v-model="url"
                    placeholder="Image URL: e.g. http://...jpg"
                    type="text"
                    id="md-input-czbyynxyg"
                    class="md-input"
                  />
                </div>
              </div>
            </div>
            <div class="md-layout">
              <div class="md-layout-item mx-auto">
                <button
                  style="margin-right : 10px; margin-left : 10px;"
                  type="button"
                  class="md-button md-success md-theme-default"
                  v-on:click="$router.push({ query: { url: url } })"
                >
                  <div class="md-ripple">
                    <div class="md-button-content">
                      <i class="fa fa-search"></i> 検索
                    </div>
                  </div>
                </button>
                <button
                  style="margin-right : 10px; margin-left : 10px;"
                  type="button"
                  class="md-button md-primary md-theme-default"
                  v-on:click="$router.push({ query: {} })"
                >
                  <!-- v-on:click="search_random()" -->
                  <div class="md-ripple">
                    <div class="md-button-content">ランダム</div>
                  </div>
                </button>
                <button
                  style="margin-right : 10px; margin-left : 10px;"
                  type="button"
                  class="md-button md-theme-default"
                  v-on:click="classicModal = true"
                  v-if="url != null"
                >
                  <div class="md-ripple">
                    <div class="md-button-content">画像操作</div>
                  </div>
                </button>
              </div>
            </div>
          </form>
          <div class="md-layout">
            <div class="md-layout-item mx-auto" v-if="this.url != null">
              <br />
              <img
                v-bind:src="url"
                style="height:150px; margin-right : 10px; margin-left : 10px;"
                alt="Image"
                class="img-raised img-fluid"
              />

              <img
                v-bind:src="crop_dataurl"
                style="height:150px; margin-right : 10px; margin-left : 10px;"
                alt="Image"
                class="img-raised img-fluid"
                v-if="crop_dataurl != null"
              />
            </div>
          </div>

          <modal v-if="classicModal" @close="classicModalHide">
            <template slot="header">
              <md-button
                class="md-simple md-just-icon md-round modal-default-button"
                @click="classicModalHide"
              >
                <md-icon>clear</md-icon>
              </md-button>
            </template>

            <template slot="body">
              <br />
              <div style="height:400px;">
                <vue-cropper
                  ref="cropper"
                  :guides="true"
                  :view-mode="2"
                  drag-mode="crop"
                  :auto-crop-area="1"
                  :min-container-width="250"
                  :min-container-height="180"
                  :background="true"
                  :rotatable="true"
                  :src="url"
                  alt="Source Image"
                  :img-style="{ height: '400px' }"
                >
                </vue-cropper>
              </div>
              <br />

              <div class="md-layout">
                <div class="md-layout-item mx-auto">
                  <button
                    style="margin-right : 10px; margin-left : 10px;"
                    type="button"
                    class="md-button md-success md-theme-default "
                    v-on:click="
                      crop_dataurl = $refs.cropper
                        .getCroppedCanvas()
                        .toDataURL();
                      $router.push({
                        query: { url: url, dataurl: crop_dataurl }
                      });
                    "
                  >
                    <div class="md-ripple">
                      <div class="md-button-content">
                        <i class="fa fa-search"></i> 検索
                      </div>
                    </div>
                  </button>
                  <button
                    style="margin-right : 10px; margin-left : 10px;"
                    type="button"
                    class="md-button md-primary md-theme-default"
                    @click="rotate"
                  >
                    <div class="md-ripple">
                      <div class="md-button-content">回転</div>
                    </div>
                  </button>
                </div>
              </div>
            </template>
          </modal>

          <br />
          <br />
          <div class="md-layout">
            <div class="md-layout-item mx-auto" v-if="this.loading">
              <br />
              <img
                width="45px"
                src="https://secure.moneypak.com/cmsfolder/content/images/ring-alt_1.gif"
              />
              <br />
            </div>
          </div>

          <div class="md-layout">
            <div
              class="md-layout-item md-size-20 md-xsmall-size-100"
              v-for="(item, i) in items"
              :key="i"
            >
              <router-link
                v-bind:to="{ name: 'search', query: { url: item.thumbnail } }"
                ><img
                  v-bind:src="item.thumbnail"
                  alt="Image"
                  class="img-raised img-fluid"
              /></router-link>

              <h4>{{ item.label }}</h4>
              <p>
                <span>
                  <md-progress-bar
                    v-if="item.score"
                    class="md-info"
                    :md-value="item.score * 100"
                  >
                  </md-progress-bar
                  ><md-tooltip md-direction="top"
                    >類似度: {{ Math.ceil(item.score * 100) }}%</md-tooltip
                  >
                </span>

                <router-link
                  v-bind:to="{
                    name: 'search',
                    query: {
                      where_metadata_label: metadata.label,
                      where_metadata_value: metadata.value
                    }
                  }"
                  v-for="(metadata, j) in item.metadata"
                  v-bind:key="j"
                >
                  <badge type="default"
                    >{{ metadata.label }}: {{ metadata.value }}</badge
                  >&nbsp;
                </router-link>

                <br v-if="item.metadata.length > 0" />

                <md-button
                  v-on:click="$router.push({ query: { url: item.thumbnail } })"
                  class="md-just-icon md-simple md-dribbble"
                >
                  <i class="material-icons">search</i>
                </md-button>
                <md-button
                  target="_blank"
                  :href="item.url"
                  class="md-just-icon md-simple md-twitter"
                >
                  <i class="material-icons">open_in_new</i>
                </md-button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Badge } from "@/components";
import { Slider } from "@/components";
import { Modal } from "@/components";
// Local
import VueCropper from "vue-cropperjs";
import "cropperjs/dist/cropper.css";
export default {
  components: {
    Badge,
    Slider,
    VueCropper,
    Modal
  },
  bodyClass: "profile-page",
  data() {
    return {
      url: null,
      items: [],
      number: 60,
      loading: true,
      //prefix: "http://localhost:5001",
      prefix: "http://portal-i.dl.itc.u-tokyo.ac.jp",
      crop_dataurl: null,
      classicModal: false
    };
  },
  props: {
    header: {
      type: String,
      default: require("@/assets/img/bg7.jpg")
    }
  },
  watch: {
    $route() {
      this.search();
    }
  },
  computed: {
    headerStyle() {
      return {
        backgroundImage: `url(${this.header})`
      };
    }
  },
  methods: {
    search: function() {
      this.url = null;
      this.crop_dataurl = null;

      this.classicModal = false;

      let param = Object.assign({}, this.$route.query);

      this.loading = true;
      this.items = [];

      if (param.where_metadata_label) {
        this.search_metadata(
          param.where_metadata_label,
          param.where_metadata_value
        );
      } else if (param.url) {
        this.url = param.url;
        if (param.dataurl) {
          this.crop_dataurl = param.dataurl;
          this.search_url(param.dataurl);
        } else {
          this.search_url(param.url);
        }
      } else {
        this.search_random();
      }
    },
    search_random: function() {
      const path = this.prefix + `/api/random`;

      var params = {};
      params.rows = this.number;

      axios.get(path, { params }).then(response => {
        this.loading = false;
        this.items = response.data;
      });
    },
    search_url: function(url) {
      var params = {};
      params.url = url;
      params.rows = this.number;

      const path = this.prefix + `/api/asearch`; //this.prefix+`/api/search`;
      axios.get(path, { params }).then(response => {
        this.loading = false;
        this.items = response.data;
      });
    },
    search_metadata: function(label, value) {
      var params = {};
      params.where_metadata_label = label; //this.$route.query.where_metadata_label;
      params.where_metadata_value = value; //this.$route.query.where_metadata_value;
      params.rows = this.number;

      const path = this.prefix + `/api/msearch`;
      axios.get(path, { params }).then(response => {
        this.loading = false;
        this.items = response.data;
      });
    },
    rotate() {
      // guess what this does :)
      this.$refs.cropper.rotate(90);
    },
    classicModalHide() {
      this.classicModal = false;
    }
  },
  created() {
    this.search();
  }
};
</script>

<style lang="scss" scoped>
.page-header {
  height: 200px !important;
}
</style>
