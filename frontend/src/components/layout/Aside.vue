<template>
  <aside>
    <div class="aside-wrap">
      <div class="aside_section first_section">
        <div class="user_info_wrap">
          <div class="u_logo"></div>
          <div class="u_info">
            <p id="ad_list_cate" href="javascript:void(0);" v-on:click="onClick" v-bind:class="{active: isActive}">{{ selectFbAdAccount.name }}</p>
            <p>{{ selectFbAdAccount.account_id }}</p>
          </div>
        </div>
        <div class="user_ad_list">
          <div class="ad_list_category" v-show="isShowList">
            <div class="ad_search_wrap">
              <input type="text" placeholder="광고주명을 입력하세요" class="ad_search_box" v-model="searchName">
              <button class="ad_submit"></button>
            </div>
            <div class="ad_search_list">
              <ul>
                <li v-for="fbAdAccount in fbAdAccountList" :key="fbAdAccount.id" @click="onClickFbAdAccount(fbAdAccount)">
                  <div class="list_image"></div>
                  <div class="list_info">
                    <strong>{{ fbAdAccount.name }}</strong>
                    <div>계정번호 : {{ fbAdAccount.account_id }}</div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="section_tab_widget clearfix">
        <ul>
          <li rel="section_list_1" class="aside_section active"><router-link v-bind:to="{ path: '/pick' }"></router-link></li>
          <li rel="section_list_2" class="aside_section"><router-link v-bind:to="{ path: '/report' }"></router-link></li>
          <li rel="section_list_3" class="aside_section"><router-link v-bind:to="{ path: '/library' }"></router-link></li>
        </ul>
      </div>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'Aside',

  data () {
    return {
      isActive: false,
      isShowList: false,
      searchName: '',
      selectFbAdAccount: {},
      fbAdAccounts: []
    }
  },

  mounted () {
    this.loadFbAdAccount()
  },

  computed: {
    fbAdAccountList: function () {
      let searchName = this.searchName
      if (searchName !== '') {
        return this.fbAdAccounts.filter(function(value) {
          if ((value.name).indexOf(searchName) > -1) {
            return value
          }
        })
      } else {
        return this.fbAdAccounts
      }
    }
  },

  methods: {
    onClick: function () {
      this.isActive = !this.isActive
      this.isShowList = !this.isShowList
    },

    loadFbAdAccount: function () {
      this.$http.get('api/fb_ad_accounts/')
      .then(res => {
        const response = res.data
        const data = response.data
        const success = response.success

        if (success === "YES") {
          if (data.length > 0) {
            this.selectFbAdAccount = data[0]
            this.fbAdAccounts = data
          }
        } else {
          throw('success: ' + success)
        }
      })
      .catch(err => {
        console.error('api/fb_ad_accounts/', err)
      })
    },

    onClickFbAdAccount: function (fbAdAccount) {
      this.selectFbAdAccount = fbAdAccount
      this.isActive = false
      this.isShowList = false
    }
  }
}
</script>

<style lang="css" scoped>
</style>
