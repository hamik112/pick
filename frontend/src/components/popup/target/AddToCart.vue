<template>
  <div class="target_contents_wrap pop-scroll clearfix" v-if="isShow">
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
            <div class="contents_title">사용픽셀</div>
            <ui-select :selectData="adAccountPixels" data-key="adAccountPixels" :onClick="selectOnClick"></ui-select>
          </div>
          <div class="use_date">
            <div>수집기간 : 최근</div>
            <div><input type="text" v-model="addToCartDay"><span>일</span></div>
          </div>
        </div>
        <div class="target_name">
          <div class="contents_title">타겟이름</div>
          <div><input type="text" v-model="addToCartName"></div>
        </div>
        <div class="target_data">
          <div class="contents_title">타겟 모수</div>
          <div>
            <span>12,000</span>명
          </div>
        </div>
      </div>
      <div class="target_tbody">
        <div class="target_inner_tbody clearfix">
          <div class="target_generate">
            <div class="account_info">
              <div class="account_title">"장바구니 이용자" 중</div>
              <div>
                <ui-select :selectData="this.selectAddToCartUser" data-key="selectAddToCartUser" :onClick="selectOnClick"></ui-select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="btn_wrap">
      <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
      <button class="next_btn" @click="createAddToCart()" v-if="makeType == 'add'">타겟 만들기</button>
      <button class="next_btn" @click="createAddToCart()" v-if="makeType == 'modify'">수정</button>
      <button class="delete_btn">삭제</button>
    </div>
  </div>
</template>

<script>
import Select from '@/components/ui/Select'

export default {
  name: 'AddToCart',

  components: {
    'ui-select': Select
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
          textList: [
            '불러오는 중 입니다.'
          ]
        }
      }
    },
    tabMove: {
      type: Function
    },
    makeType: {
      type:String
    }
  },

  data () {
    return {
      addToCartDay: '30',
      addToCartName: '',

      subSelect:false,
      subInput:false,

      selectAddToCartUser: {
        emptyText: '전체 고객',
        textList: [
          '전체 고객',
          '미 구매 고객'
        ],
        keyList: [
          'total',
          'non_purchase'
        ]
      }
    }
  },

  methods: {
    selectOnClick (item) {
      const key = event.target.closest('.select_btn').getAttribute('data-key')
      const textCheck = item.replace(/\s/gi, "")

      this[key].emptyText = item
    },

    findSelectKey (selectName) {
      /*
      Select Key 가져오기
      */
      const emptyText = this[selectName].emptyText
      const textList = this[selectName].textList
      const keyList = this[selectName].keyList
      return keyList[textList.indexOf(emptyText)]
    },

    createAddToCart () {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'add_to_cart',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.addToCartName,
        retention_days: this.addToCartDay,

        detail: this.findSelectKey('selectAddToCartUser')
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
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
