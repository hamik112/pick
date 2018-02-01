<template>
  <aside>
    <div class="aside-wrap">
      <div class="aside_section first_section">
        <div class="user_info_wrap">
          <div class="u_mask"></div>
          <div class="u_logo"><img src="../../assets/images/icon/user_logo_type01.png" alt=""></div>
          <div class="u_info">
            <div class="u_info_box">
              <pre id="ad_list_cate" href="javascript:void(0);" @click="onClick()" v-bind:class="{active: isActive}">{{ selectedFbAdAccount.name }}</pre>
              <pre>{{ selectedFbAdAccount.account_id }}</pre>
            </div>
            <div class="user_ad_list">
              <div class="ad_list_category" v-show="isShowList">
                <div class="ad_search_wrap">
                  <input type="text" placeholder="광고주명을 입력하세요" class="ad_search_box" v-model="searchName">
                  <button class="ad_submit"></button>
                </div>
                <div class="ad_search_list">
                  <ul>
                    <li v-for="fbAdAccount in fbAdAccountList" :key="fbAdAccount.id" @click.stop="selectFbAdAccount(fbAdAccount)">
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
      // show: false,
      isActive: false,
      isShowList: false,
      searchName: '',
      selectedFbAdAccount: {},
      fbAdAccounts: []
    }
  },

  created () {
    this.$eventBus.$on('pickdataLogin', this.loadFbAdAccounts)
  },

  mounted () {
    // DEBUG mounted
    this.loadFbAdAccounts()
  },

  beforeDestroy () {
    this.$eventBus.$off('pickdataLogin', this.loadFbAdAccounts)
  },

  watch: {
    // '$route' (to, from) {
    //   console.log(to)
    //   console.log(from)
    // }
  },

  computed: {
    fbAdAccountList () {
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
    onClick (e) {
      this.isActive = !this.isActive
      this.isShowList = !this.isShowList
      document.addEventListener('click', this.dc)
    },
    dc(e) {
      const check = this.$el.contains(e.target)
      if(check === false) {
        this.stopEvent()
      }
      this.isActive = check
      this.isShowList = check

    },
    stopEvent() {
      document.removeEventListener('click', this.dc)
    },

    findFbAdAccountByAccountId (fbAdAccounts, accountId) {
      let result = fbAdAccounts[0]
      if (typeof accountId === typeof undefined || accountId == null) {
        return result
      } else {
        fbAdAccounts.forEach(function (fbAdAccount, index) {
          if (fbAdAccount.account_id === localStorage.getItem('account_id')) {
            result = fbAdAccount
          }
        })
      }
      return result
    },

    // 페이스북 광고 계정 로드
    loadFbAdAccounts (res) {
      // 페이스북 광고 계정 리스트 가져오기
      this.$http.get('/fb_ad_accounts/')
      .then(res => {
        const response = res.data
        const data = response.data
        const success = response.success

        if (success === "YES") {
          // 데이터가 존재 할 때
          if (data.length > 0) {
            // 페이스북 광고 계정 리스트
            this.fbAdAccounts = data
            let defaultAccount = this.findFbAdAccountByAccountId(this.fbAdAccounts, localStorage.getItem('account_id'))

            // 현재 페이스북 광고 계정 설정
            this.$store.state.currentFbAdAccount = defaultAccount
            this.selectedFbAdAccount = defaultAccount

            // this.$eventBus.$emit('getTargetPick', this.selectedFbAdAccount)
            this.selectFbAdAccount(defaultAccount)
          }
        } else {
          throw('success: ' + success)
        }
      })
      .catch(err => {
        console.error('/fb_ad_accounts/', err)
      })
    },

    // 페이스북 광고 계정 선택
    selectFbAdAccount (fbAdAccount) {
      // 현재 페이스북 광고 계정 설정
      this.$store.state.currentFbAdAccount = fbAdAccount
      this.selectedFbAdAccount = fbAdAccount
      // 리스트 속성
      this.isActive = false
      this.isShowList = false

      // 페이스북 광고 계정 아이디 찾기위한 로직
      this.$http.get('/fb_ad_accounts/confirm_ad_account', {
        params: {
          act_account_id: fbAdAccount.id
        }
      })
      .then(res => {
        // 선택된 페이스북 광고 계정 아이디 저장
        localStorage.setItem('fb_ad_account_id', res.data.fb_ad_account.fb_ad_account_id)
        localStorage.setItem('account_id', fbAdAccount.account_id)
        localStorage.setItem('account_name', fbAdAccount.name)

        // 페이스북 광고 계장 정보 갱신
        this.$eventBus.$emit('getFbAdAccountInfo')
        // Target Pick 갱신
        this.$eventBus.$emit('getTargetPick', fbAdAccount)
      })
    }
  }
}
</script>

<style lang="css" scoped>
</style>
