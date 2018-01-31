<template>
  <div id="tab-list-1" class="basic-tab-contents category_setup clearfix">
    <transition name="modal">
      <ui-dialog :dialogData="dialogData" v-if='dialogShow' @ok='dialogOk' @cancel="dialogCancel"></ui-dialog>
    </transition>
    <div class="cate_prologue">
      <strong>현재 선택된 광고 계정의 카테고리와 사용할 픽셀을 지정해 주세요.</strong>
      <p>맞춤 타겟 생성 및 통계 분석을 위해 반드시 선택해 주세요.</p>
    </div>
    <div class="cate_contents_widget">
      <ul class="target_pick_01">
        <li @click="selectCategory('보험')" v-bind:class="[this.categoryName === '보험' ? 'Click_on' : '']">
          <span>보험</span>
        </li>
        <li @click="selectCategory('대출')" v-bind:class="[this.categoryName === '대출' ? 'Click_on' : '']">
          <span>대출</span>
        </li>
        <li @click="selectCategory('카드')" v-bind:class="[this.categoryName === '카드' ? 'Click_on' : '']">
          <span>카드</span>
        </li>
        <li @click="selectCategory('NGO')" v-bind:class="[this.categoryName === 'NGO' ? 'Click_on' : '']">
          <span>NGO</span>
        </li>
      </ul>
      <ul class="target_pick_02">
        <li @click="selectCategory('쇼핑몰')" v-bind:class="[this.categoryName === '쇼핑몰' ? 'Click_on' : '']">
          <span>쇼핑몰</span>
        </li>
        <li @click="selectCategory('여행')" v-bind:class="[this.categoryName === '여행' ? 'Click_on' : '']">
          <span>여행</span>
        </li>
        <li @click="selectCategory('뷰티')" v-bind:class="[this.categoryName === '뷰티' ? 'Click_on' : '']">
          <span>뷰티</span>
        </li>
        <li @click="selectCategory('기타')" v-bind:class="[this.categoryName === '기타' ? 'Click_on' : '']">
          <span>기타</span>
        </li>
      </ul>
      </div>
      <div class="pixel_info">
          <div class="pixel_info_title">사용픽셀</div>
          <div v-if="subPixel">
          <ui-select :selectData="this.usingPixel" data-key="usingPixel" :pixelIdShow="subPixel" :onClick="selectOnClick"></ui-select>
      </div>
    </div>
    <div class="btn_wrap">
      <button type="button" class="next_btn" @click="confirm()">다음</button>
    </div>
  </div>
</template>

<script>
import Select from '@/components/ui/Select'
import Dialog from '@/components/ui/Dialog'

export default {
  components:{
    'ui-dialog': Dialog,
    'ui-select': Select
  },

	created () {
    // 사용픽셀 리스트
		this.$http.get('/fb_ad_accounts/ad_account_pixels', {
			params: {
			  act_account_id: this.currentFbAdAccount.id
	  	}
	  })
		.then(res => {
			const data = res.data.data

			for(let i = 0; i < data.length; i++) {
				this.usingPixel.textList.push(data[i].name)
        this.usingPixel.pixelId.push(data[i].id)
      }

      return this.usingPixel
    })
    .then(usingPixel => {
      const fbAdAccountId = localStorage.getItem('fb_ad_account_id')

      if(fbAdAccountId === 'undefined') {
        // 설정전
        this.usingPixel.emptyText = usingPixel.textList[0]
        this.usingPixel.emptyTextId = usingPixel.pixelId[0]
      } else {
        // 설정후(=수정)
        this.$http.get('/fb_ad_accounts/' + fbAdAccountId + '/')
        .then(res => {
          const data = res.data
          this.categoryName = data.account_category_name

          const usingPixelIndex = this.usingPixel.pixelId.indexOf(data.fb_ad_account.pixel_id.toString())
          this.usingPixel.emptyText = this.usingPixel.textList[usingPixelIndex]
          this.usingPixel.emptyTextId = data.fb_ad_account.pixel_id
        })
      }
    })
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
      usingPixel: {
		    emptyText: '',
		    emptyTextId: '',
		    textList: [],
		    pixelId: []
	    },
      categoryName: '',
      subPixel:true
    }
  },

  computed: {
    currentFbAdAccount() {
        return this.$store.state.currentFbAdAccount
    }
  },

  methods: {
    selectOnClick (item) {
      const key = event.target.closest('.select_btn').getAttribute('data-key')
      const textCheck = item.replace(/\s/gi, "")
      const pixelIdText = (event.target.childNodes[1].className === 'text-span') ? event.target.childNodes[1].innerText:'error'
      this[key].emptyTextId = pixelIdText
      this[key].emptyText = item
    },

    dialogOpen(emptyText, type, mode) {
      this.dialogData['emptyText'] = emptyText
      this.dialogData['type'] = type
      this.dialogData['mode'] = mode
      this.dialogShow = true;
    },
    dialogOk() {
      const mode = this.dialogData.mode

      //모드별 동작

      this.nextStage = true
      this.dialogShow = false;
    },
    dialogCancel() {
      this.nextStage = false;
      this.dialogShow = false;
    },

    selectCategory (name) {
      this.categoryName = name
    },

    confirm () {
      if (this.categoryName === '') {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('통계 및 계정 유형 분석을 선택해주세요.', 'alert')
      } else {
        if(this.categoryName === '대출') {
          this.accountCategoryId = 1
        } else if(this.categoryName === 'NGO') {
          this.accountCategoryId = 2
        } else if(this.categoryName === '카드') {
          this.accountCategoryId = 3
        } else if(this.categoryName === '여행') {
          this.accountCategoryId = 4
        } else if(this.categoryName === '쇼핑몰') {
          this.accountCategoryId = 5
        } else if(this.categoryName === '기타') {
          this.accountCategoryId = 6
        } else if(this.categoryName === '보험') {
          this.accountCategoryId = 7
        } else if(this.categoryName === '뷰티') {
          this.accountCategoryId = 8
        }

        let currentStep = [false, true, false]
        this.$emit('setCategory', currentStep, this.accountCategoryId, this.usingPixel.emptyTextId)
      }
    },
  }
}
</script>

<style>

</style>
