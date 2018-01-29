<template>
	<header>
		<transition name="modal">
		  <ui-dialog :dialogData="dialogData" v-if='dialogShow' @ok='dialogOk' @cancel="dialogCancel"></ui-dialog>
		</transition>
		<div class="left_area"><a href="#/"><img src="../../assets/images/common/main_logo.jpg" alt="pickdata" /></a></div>
		<div class="right_area">
			<div class="user">
				<p class="user_mask"></p>
				<p class="user_image"><img v-bind:src="userImage" alt=""></p>
				<p>{{ userName }}</p>
			</div>
			<div class="user_setup">
				<p id="set_up"><router-link v-bind:to="{ path: '/setting' }"><img src="../../assets/images/icon/set_up_btn.png" alt="톱니바퀴" /></router-link></p>
				<p><a href="javascript:void(0)" @click="logoutBtn"><img src="../../assets/images/icon/logout_i.png" alt="문" /></a></p>
			</div>
		</div>
	</header>
</template>

<script>
import { getUserName, getUserImage } from '../../utils/auth'
import Dialog from '@/components/ui/Dialog'

export default {
	name: 'Header',
	components:{
		'ui-dialog': Dialog
	},
	mounted () {
		this.userName = getUserName()
		this.userImage = getUserImage()
	},

	data () {
		return {
		  dialogShow:false,
	      dialogData:{
	        emptyText:'sample',
	        type:'confirm',
	        mode:'sample'
	      },
	      nextStage:false,
			setupOn: false,
			userName: '',
			userImage: ''
		}
	},

	methods: {
		dialogOpen(emptyText, type, mode) {
	      this.dialogData['emptyText'] = emptyText
	      this.dialogData['type'] = type
	      this.dialogData['mode'] = mode
	      this.dialogShow = true;
	    },
	    dialogOk() {
	      const mode = this.dialogData.mode
	      //모드별 동작
	      if(mode == 'logout') {
	      	this.logout()
	      }
	      this.nextStage = true
	      this.dialogShow = false;
	    },
	    dialogCancel() {
	      this.nextStage = false;
	      this.dialogShow = false;
	    },
		logoutBtn () {
			//컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
      		this.dialogOpen('픽데이터에서 로그아웃 하시겠습니까?', 'confirm', 'logout')
		},
		logout() {
			this.$http.get('/users/signout')
			.then(res => {
				const success = res.data.success
				if (success === 'YES') {
					// logoput
					this.$router.push({name: 'Intro'})
				} else {
					// except
					console.log('msg', res.data.msg)
					return
				}
			})
			.catch(err => {
				console.error('/users/signout', err)
				return
			})
		}
	}
}
</script>

<style lang="css" scoped>
</style>
