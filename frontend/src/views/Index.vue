<template>
  <div class="wrapper">
    <parallax class="section page-header header-filter" :style="headerStyle">
      <div class="container">
        <div class="md-layout">
          <div class="md-layout-item">
            <h1 class="title">東京大学学術資産等アーカイブズポータル<br/>画像検索
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
              <h5 class="description">&nbsp;&nbsp;<a href="http://image-net.org/challenges/LSVRC/2012/">ImageNet 2012</a>で訓練された<a href="https://www.cs.unc.edu/~wliu/papers/GoogLeNet.pdf">Inception</a> Convolutional Neural Networkを用いて抽出した特徴量の<a href="https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximate_nearest_neighbor">近似最近傍</a>に基づく類似度を使用しています。</h5>
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
            "https://da.dl.itc.u-tokyo.ac.jp/portal/sites/default/files/images/assets/1333099054093.jpg"
        },
        {
          thumbnail:
            "https://da.dl.itc.u-tokyo.ac.jp/portal/sites/default/files/images/assets/1332747896774.jpg"
        },
        {
          thumbnail:
            "https://da.dl.itc.u-tokyo.ac.jp/portal/sites/default/files/images/assets/miyake/f84c5dab77dd8daaf693d846309ddc8f.jpg"
        },
        {
          thumbnail:
            "https://da.dl.itc.u-tokyo.ac.jp/portal/sites/default/files/images/assets/kahei/0a8c63313d3739395176e7378b2a5601_0.jpg"
        },
        {
          thumbnail:
            "https://da.dl.itc.u-tokyo.ac.jp/portal/sites/default/files/images/assets/enshurin_tori/b1a2a77d-5247-4c96-9b72-e48cdbedd983.jpg"
        },
        {
          thumbnail:
            "https://da.dl.itc.u-tokyo.ac.jp/portal/sites/default/files/images/assets/tokoro/116d52d2-ffb7-4119-a8da-768ee9499e89_2.jpg"
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