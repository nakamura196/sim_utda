<template>
  <div class="wrapper">
    <parallax class="section page-header header-filter" :style="headerStyle">
      <div class="container">
        <div class="md-layout">
          <div class="md-layout-item">
            <h1 class="title">東京大学学術資産等アーカイブズポータル類似画像検索
            </h1>
            <br>
            <md-button v-bind:to="{ name : 'search'}" class="md-success md-lg">
              <i class="fas fa-search"></i>試してみる
            </md-button>
          </div>
        </div>
      </div>
    </parallax>
    <div class="main main-raised">
      <div class="section" id="about">
        <div class="container">
          <div class="md-layout">
            <div class="md-layout-item md-size-66 md-xsmall-size-100 mx-auto text-center">
              <h2 class="title text-center">About</h2>

              <h5 class="description">&nbsp;&nbsp;東京大学学術資産等アーカイブズポータルで公開されている画像を検索できます。</h5>
              <h5 class="description">&nbsp;&nbsp;ImageNet 2012で訓練されたInception Convolutional Neural Networkを用いて抽出した特徴量のコサイン類似度を使用しています。</h5>
            </div>
          </div>
        </div>
      </div>
      <div class="section" id="example">
        <div class="container">
          <div class="md-layout">
            <div class="md-layout-item md-size-66 md-xsmall-size-100 mx-auto text-center">
              <h2 class="title text-center">検索例</h2>
              <div class="md-layout">
                <div class="md-layout-item md-size-33 md-xsmall-size-100" v-for="(item, i) in items" :key="i">
                  <router-link v-bind:to="{ name : 'search', query : { url: item.thumbnail}}"><img v-bind:src="item.thumbnail" alt="Rounded Image" class="rounded img-raised img-fluid"/></router-link>
                  <h4><md-button v-bind:to="{ name : 'search', query : { url: item.thumbnail}}" class="md-just-icon md-simple md-dribbble">
                      <i class="fa fa-search"></i>
                    </md-button>
                  </h4>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  bodyClass: "landing-page",
  props: {
    header: {
      type: String,
      default: require("@/assets/img/bg7.jpg")
    }
  },
  data() {
    return {
      items: [
        {
          thumbnail:
            "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kunshujou/A00_6010/046/046_0052.tif/4117,620,2186,2324/,300/0/default.jpg"
        },
        {
          thumbnail:
            "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kunshujou/A00_6010/053/053_0162.tif/955,699,1920,1349/,300/0/default.jpg"
        },
        {
          thumbnail:
            "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kunshujou/A00_6010/049/049_0175.tif/5397,2787,2009,2541/,300/0/default.jpg"
        },
        {
          thumbnail:
            "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kunshujou/A00_6010/043/043_0100.tif/5348,2846,1093,1004/,300/0/default.jpg"
        },
        {
          thumbnail:
            "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kunshujou/A00_6010/026/026_0027.tif/3813,1735,2678,3432/,300/0/default.jpg"
        },
        {
          thumbnail:
            "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/kunshujou/A00_6010/065/065_0024.tif/5259,1940,1644,1960/,300/0/default.jpg"
        }
      ]
    };
  },
  computed: {
    headerStyle() {
      return {
        backgroundImage: `url(${this.header})`
      };
    }
  }
};
</script>
<style lang="scss" scoped>
h1, h2 {
  font-family: "Roboto", "Helvetica", "Arial", sans-serif;
}
.page-header {
    height: 70vh;
}
</style>