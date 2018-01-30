<template>
  <div class="target_contents_wrap clearfix" v-if="isShow">
    <transition name="modal">
      <ui-dialog :dialogData="dialogData" v-if="dialogShow" @ok="dialogOk()" @cancel="dialogCancel()"></ui-dialog>
    </transition>
    <div class="target_contents_inner">
      <div class="target_thead">
        <div class="main_title">
          <div><img src="../../../assets/images/target/target_logo_06.png" alt="cart"></div>
          <div class="title_info">
            <p>장바구니</p>
            <p>타겟의 속성을 정의하세요</p>
          </div>
        </div>
        <div class="use_wrap">
          <div class="use_select">
            <div class="contents_title">사용 픽셀</div>
            <ui-select :selectData="adAccountPixels" data-key="adAccountPixels" :onClick="selectOnClick"></ui-select>
          </div>
          <div class="use_date">
            <div>수집 기간 : 최근</div>
            <div><input type="text" v-model="collectionPeriod"><span>일</span></div>
          </div>
        </div>
        <div class="target_name">
          <div class="contents_title">타겟 이름</div>
          <div><input type="text" v-model="targetName"></div>
        </div>
        <div class="target_data">
          <div class="contents_title">타겟 모수</div>
          <div>
            <span>{{ this.audienceSize }}</span>
            <span v-show="isNumber">명</span>
          </div>
        </div>
      </div>
      <div class="target_tbody">
        <div class="target_inner_tbody clearfix">
          <div class="target_generate">
            <div class="account_info">
              <div class="account_title">"장바구니 이용자" 중</div>
              <div>
                <ui-select :selectData="this.selectCustomer" data-key="selectCustomer" :onClick="selectOnClick"></ui-select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="makeType === 'modify'">* 설정 수정시 기존 생성된 타겟과 병합되어 모수가 중복될 수 있습니다. 특별한 상황이 아니면 설정의 수정을 지양해주세요.</div>
    <div class="btn_wrap">
      <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
      <button class="next_btn" @click="createAddToCartTarget()" v-if="makeType === 'add'">타겟 만들기</button>
      <button class="delete_btn" @click="deleteAddToCartTarget()" v-if="makeType === 'modify'">삭제</button>
      <button class="next_btn" @click="updateAddToCartTarget()" v-if="makeType === 'modify'">타겟 수정하기</button>
    </div>
  </div>
</template>

<script>
import { numberFormatter } from '@/components/utils/Formatter'
import Select from '@/components/ui/Select'
import Dialog from '@/components/ui/Dialog'

export default {
  name: 'AddToCart',

  components: {
    'ui-select': Select,
    'ui-dialog': Dialog
  },

  props: {
    isShow: {
      type: Boolean,
      default () {
        return false
      }
    },

    adAccountPixels: {
      type: Object,
      default () {
        return {
          emptyText: '불러오는 중 입니다.',
          textList: [ '불러오는 중 입니다.' ]
        }
      }
    },
    
    tabMove: {
      type: Function
    },

    makeType: {
      type:String
    },

    makeItem: {
      type: Object
    }
  },

  created () {
    this.$eventBus.$on('modifyAddToCartTarget', this.modifyAddToCartTarget)
  },

  beforeDestroy () {
    this.$eventBus.$off('modifyAddToCartTarget', this.modifyAddToCartTarget)
  },

  data () {
    return {
      collectionPeriod: '30',
      targetName: '',
      audienceSize: '-',
      isNumber: false,

      subSelect:false,
      subInput:false,

      dialogShow: false,
      dialogData: {
        emptyText:'sample',
        type:'confirm',
        mode:'sample'
      },

      selectCustomer: {
        emptyText: '전체 고객',
        textList: [
          '전체 고객',
          '미구매 고객'
        ],
        keyList: [
          'total',
          'non_purchase'
        ]
      }
    }
  },

  methods: {
    dialogOpen (emptyText, type, mode) {
      this.dialogData['emptyText'] = emptyText
      this.dialogData['type'] = type
      this.dialogData['mode'] = mode
      this.dialogShow = true;
    },

    // 다이얼로그 확인 클릭시
    dialogOk () {
      const mode = this.dialogData.mode

      if(mode === 'createAddToCartTarget') {
        // Create Target -----------------------------------------------------------------
        let params = {
          fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
          target_type: 'add_to_cart',
          pixel_id: this.findSelectKey('adAccountPixels'),
          name: this.targetName,
          retention_days: this.collectionPeriod,

          detail: this.findSelectKey('selectCustomer')
        }

        this.$http.post('/pickdata_account_target/custom_target', params)
        .then((response) => {
          var success = response.data.success;
          if (success == "YES") {
            // success
            this.$eventBus.$emit('getAccountTarget')
          } else {
            alert('장바구니 타겟 생성 실패')
            throw('success: ' + success)
          }
          this.$emit('close')
        })
        .catch(err => {
          this.$emit('close')
          console.log('/pickdata_account_target/custom_target: ', err)
        })

      } else if (mode === 'deleteAddToCart') {
        // Delete Target -----------------------------------------------------------------
        this.$emit('deleteCustomTarget', this.makeItem.id)

      } else if (mode === 'updateAddToCart') {
        // Update Target -----------------------------------------------------------------
        let params = {
          pickdata_account_target_id: this.makeItem.id,
          fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
          target_type: 'add_to_cart',
          pixel_id: this.findSelectKey('adAccountPixels'),
          name: this.targetName,
          retention_days: this.collectionPeriod,

          detail: this.findSelectKey('selectCustomer'),
        }

        this.$http.put('/pickdata_account_target/custom_target', params)
        .then((response) => {
          var success = response.data.success
          if (success == "YES") {
            // success
            this.$eventBus.$emit('getAccountTarget')
          } else {
            alert('장바구니 타겟 생성 실패')
            throw('success: ' + success)
          }
          this.$emit('close')
        })
        .catch(err => {
          this.$emit('close')
          console.log('/pickdata_account_target/custom_target delete: ', err)
        })
      }

      // 모드별 동작
      this.nextStage = true
      this.dialogShow = false;
    },

    // 다이얼로그 취소 클릭시
    dialogCancel () {
      this.nextStage = false;
      this.dialogShow = false;
    },

    selectOnClick (item) {
      const key = event.target.closest('.select_btn').getAttribute('data-key')
      const textCheck = item.replace(/\s/gi, "")

      this[key].emptyText = item
    },

    findSelectText (selectName, key) {
      // Select Text 가져오기
      const textList = this[selectName].textList
      const keyList = this[selectName].keyList
      return textList[keyList.indexOf(key)]
    },

    findSelectKey (selectName) {
      // Select Key 가져오기
      const emptyText = this[selectName].emptyText
      const textList = this[selectName].textList
      const keyList = this[selectName].keyList
      return keyList[textList.indexOf(emptyText)]
    },

    // Create Target Dialog
    createAddToCartTarget () {
      this.dialogOpen('입력한 내용으로 타겟을 생성하겠습니까?', 'confirm', 'createAddToCartTarget')
    },

    // Delete Target Dialog
    deleteAddToCartTarget () {
      this.dialogOpen('삭제하시겠습니까?', 'confirm', 'deleteAddToCart')
    },

    // Update Target Dialog
    updateAddToCartTarget () {
      this.dialogOpen('수정하시겠습니까?', 'confirm', 'updateAddToCart')
    },

    // 수정 클릭시 타겟 생성 팝업 데이터 초기화 (/fb_ad_accounts/ad_account_pixels call after)
    modifyAddToCartTarget () {
      const description = this.makeItem.description
      const params = description.params
      const detail = params.detail

      // 사용 픽셀
      this.adAccountPixels.emptyText = this.findSelectText('adAccountPixels', params.pixel_id)

      // 수집 기간
      this.collectionPeriod = numberFormatter(description.retention_days)

      // 타겟 이름
      this.targetName = this.makeItem.name

      // 타겟 모수
      const displayCount = this.makeItem.display_count

      if (displayCount === '규모가 적음') {
        this.audienceSize = displayCount
        this.isNumber = false
      } else if (displayCount === '생성중') {
        this.audienceSize = displayCount
        this.isNumber = false
      } else {
        this.audienceSize = numberFormatter(this.makeItem.display_count)
        this.isNumber = true
      }

      // 장바구니 이용자중 @
      if (detail === 'total') {
        // 전체 고객
        this.selectCustomer.emptyText = '전체 고객'
      } else if (detail === 'non_purchase') {
        // 미구매 고객
        this.selectCustomer.emptyText = '미구매 고객'
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
