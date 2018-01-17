<template>
  <aside>
  	<transition name='modal'>
  		<!-- <TargetNot v-if="show" @close="show = false"></TargetNot> -->
  	</transition>
	<div class="aside-wrap">
	  <div class="aside_section first_section">
		<div class="user_info_wrap">
		  <div class="u_mask"></div>
		  <div class="u_logo"><img src="../../assets/images/common/test_img.jpg" alt=""></div>
		  <div class="u_info">
			<pre id="ad_list_cate" href="javascript:void(0);" v-on:click="onClick" v-bind:class="{active: isActive}">{{ selectFbAdAccount.name }}</pre>
			<pre>{{ selectFbAdAccount.account_id }}</pre>
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
		  <li rel="section_list_1" class="aside_section active" @click="show = true"><router-link v-bind:to="{ path: '/pick' }"></router-link></li>
		  <li rel="section_list_2" class="aside_section"><router-link v-bind:to="{ path: '/report' }"></router-link></li>
		  <li rel="section_list_3" class="aside_section"><router-link v-bind:to="{ path: '/library' }"></router-link></li>
		</ul>
	  </div>
	</div>

  </aside>
</template>

<script>
	// 팝업
	import TargetNot from '@/components/popup/Target_not_available'

export default {
  name: 'Aside',
  components:{
  	// 'TargetNot' : TargetNot
  },
  data () {
	return {
		// show: false,
		isActive: false,
		isShowList: false,
		searchName: '',
		selectFbAdAccount: {},
		fbAdAccounts: []
	}
  },

  created () {
	this.$eventBus.$on('pickdataLogin', this.loadFbAdAccount)
  },

  mounted () {
	// DEBUG mounted
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

	loadFbAdAccount: function (res) {
	  if (res == null) {
		console.log('DEBUG Call')
	  }
	  console.log('loadFbAdAccount', res)
	  this.$http.get('/api/fb_ad_accounts/')
	  .then(res => {
		const response = res.data
		const data = response.data
		const success = response.success

		if (success === "YES") {
		  if (data.length > 0) {
			// Vuex state
			this.$store.state.currentFbAdAccount = data[0]
			
			this.selectFbAdAccount = data[0]
			this.fbAdAccounts = data
			this.$eventBus.$emit('selectFbAdAccount', this.selectFbAdAccount)
		  }
		} else {
		  throw('success: ' + success)
		}
	  })
	  .catch(err => {
		console.error('/api/fb_ad_accounts/', err)
	  })
	},

	onClickFbAdAccount: function (fbAdAccount) {
		// Vuex state
		this.$store.state.currentFbAdAccount = fbAdAccount

	  this.$eventBus.$emit('selectFbAdAccount', fbAdAccount)
	  this.selectFbAdAccount = fbAdAccount
	  this.isActive = false
	  this.isShowList = false
    localStorage.setItem('account_id', fbAdAccount.account_id)
	}
  }
}
</script>

<style lang="css" scoped>
</style>
