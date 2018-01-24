<template>
  <div class="modal-mask">
    <div class="modal-wrapper">
      <div class="modal-container">
        <div class="layer-pop-widget">
          <div class="popup-widget" id="target_pop_01">
            <div class="popup-contents clearfix">
              <div class="pop_title_wrap">
                <div class="pop_title">타겟 만들기 (<span id="page-number">1</span>/2)</div>
                <p class="popup-btn"><button type="button" id="close-btn" class="close_pop close-btn" @click="$emit('close')"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
              </div>

              <!-- 카테고리 선택 탭 -->
              <div class="pop_tab_wrap clearfix" v-if="tabAction.tabActive1.show">
                <div class="cate_contents_widget">
                  <ul class="target_pick_01">
                    <li @click="tabMove(1)">
                      <span>사이트방문</span>
                    </li>
                    <li @click="tabMove(2)">
                      <span>특정페이지 방문</span>
                    </li>
                    <li @click="tabMove(3)">
                      <span>NEO 타겟</span>
                    </li>
                    <li @click="tabMove(4)">
                      <span>구글애널리틱스</span>
                    </li>
                  </ul>
                  <ul class="target_pick_02">
                    <li @click="tabMove(5)">
                      <span>구매</span>
                    </li>
                    <li @click="tabMove(6)">
                      <span>장바구니</span>
                    </li>
                    <li @click="tabMove(7)">
                      <span>회원가입</span>
                    </li>
                    <li @click="tabMove(8)">
                      <span>단계별 전환</span>
                    </li>
                  </ul>
                </div>
                <div class="btn_wrap">
                  <button type="button" class="close_pop" @click="$emit('close')">취소</button>
                </div>
              </div>

              <!-- 사이트 방문 탭 -->
              <visit-site
              :isShow="tabAction.tabActive2.show"
              :adAccountPixels="this.adAccountPixels"
              :tabMove="tabMove"
              :makeType="this.makeType"
              :makeItem="this.makeItem"
              @close="$emit('close')"></visit-site>

              <!-- 특정 페이지 방문 탭 -->
              <visit-specific-pages
              :isShow="tabAction.tabActive3.show"
              :adAccountPixels="this.adAccountPixels"
              :tabMove="tabMove"
              :makeType="this.makeType"
              :makeItem="this.makeItem"
              @close="$emit('close')"></visit-specific-pages>

              <!-- 네오 탭 -->
              <neo-target
              :isShow="tabAction.tabActive4.show"
              :adAccountPixels="this.adAccountPixels"
              :tabMove="tabMove"
              :makeType="this.makeType"
              :makeItem="this.makeItem"
              @close="$emit('close')"></neo-target>

              <!-- 구글애널리틱스 탭 -->
              <utm-target
              :isShow="tabAction.tabActive5.show"
              :adAccountPixels="this.adAccountPixels"
              :tabMove="tabMove"
              :makeType="this.makeType"
              :makeItem="this.makeItem"
              @close="$emit('close')"></utm-target>

              <!-- 구매 탭 -->
              <purchase
              :isShow="tabAction.tabActive6.show"
              :adAccountPixels="this.adAccountPixels"
              :tabMove="tabMove"
              :makeType="this.makeType"
              :makeItem="this.makeItem"
              @close="$emit('close')"></purchase>

              <!-- 장바구니 탭 -->
              <add-to-cart
              :isShow="tabAction.tabActive7.show"
              :adAccountPixels="this.adAccountPixels"
              :tabMove="tabMove"
              :makeType="this.makeType"
              :makeItem="this.makeItem"
              @close="$emit('close')"></add-to-cart>

              <!-- 회원가입 탭 -->
              <registration
              :isShow="tabAction.tabActive8.show"
              :adAccountPixels="this.adAccountPixels"
              :tabMove="tabMove"
              :makeType="this.makeType"
              :makeItem="this.makeItem"
              @close="$emit('close')"></registration>

              <!-- 단계별 전환 -->
              <conversion
              :isShow="tabAction.tabActive9.show"
              :adAccountPixels="this.adAccountPixels"
              :tabMove="tabMove"
              :makeType="this.makeType"
              :makeItem="this.makeItem"
              @close="$emit('close')"></conversion>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { numberFormatter } from '@/components/utils/Formatter'

// Popup
import VisitSite from '@/components/popup/target/VisitSite'
import VisitSpecificPages from '@/components/popup/target/VisitSpecificPages'
import NeoTarget from '@/components/popup/target/NeoTarget'
import UtmTarget from '@/components/popup/target/UtmTarget'
import Purchase from '@/components/popup/target/Purchase'
import AddToCart from '@/components/popup/target/AddToCart'
import Registration from '@/components/popup/target/Registration'
import Conversion from '@/components/popup/target/Conversion'

// UI
import Select from '@/components/ui/Select'

export default {
  name: 'TargetMake01',

  components:{
    VisitSite,
    VisitSpecificPages,
    NeoTarget,
    UtmTarget,
    Purchase,
    AddToCart,
    Registration,
    Conversion,
    'ui-select': Select,
  },

  props: {
    makeType: {
      type: String
    },
    makeItem: {
      type: Object
    }
  },

  mounted () {
    // 수정인 경우 해당 탭으로 이동 해야한다.
    if (this.makeType === 'modify') {
      const modifyItem = this.makeItem
      this.moveModifyTab(modifyItem)
    }
    let emptyText = ''
    let textList = []
    let keyList = []

    this.$http.get('/fb_ad_accounts/ad_account_pixels', {
      params: {
        'fb_ad_account_id': localStorage.getItem('fb_ad_account_id')
      }
    })
    .then(res => {
      const response = res.data
      const data = response.data
      const success = response.success
      if (success === 'YES') {
        data.forEach(function(item, index) {
          textList.push(item.name)
          keyList.push(item.id)
          if (index === 0) {
            emptyText = item.name
          }
        })

        this.adAccountPixels.emptyText = emptyText
        this.adAccountPixels.textList = textList
        this.adAccountPixels.keyList = keyList
      } else {
        console.log('/fb_ad_accounts/ad_account_pixels fail')
      }
    })
  },

  data () {
    return {
      tabAction:{
        tabActive1:{
          show:true
        },
        tabActive2:{
          show:false
        },
        tabActive3:{
          show:false
        },
        tabActive4:{
          show:false
        },
        tabActive5:{
          show:false
        },
        tabActive6:{
          show:false
        },
        tabActive7:{
          show:false
        },
        tabActive8:{
          show:false
        },
        tabActive9:{
          show:false
        }
      },

      //싱글 셀렉트
      adAccountPixels: {
        emptyText: '불러오는 중 입니다.',
        textList: [
          '불러오는 중 입니다.'
        ]
      }
    }
  },

  methods: {
    moveModifyTab (item) {
      let categoryName = item.pixel_mapping_category.category_label_en
      categoryName = categoryName.replace(/\s/gi, "")

      if (categoryName === 'visitpages') {
        // 사이트 방문
        this.tabMove(1)
      } else if (categoryName === 'visitspecificpages') {
        // 특정페이지 방문
        this.tabMove(2)
      } else if (categoryName === 'neotarget') {
        // NEO 타겟
        this.tabMove(3)
      } else if (categoryName === 'utmtarget') {
        // 구글애널리틱스
        this.tabMove(4)
      } else if (categoryName === 'purchase') {
        // 구매
        this.tabMove(5)
      } else if (categoryName === 'addtocart') {
        // 장바구니
        this.tabMove(6)
      } else if (categoryName === 'registration') {
        // 회원가입
        this.tabMove(7)
      } else {
        // 'conversioncomplete', 'conversion1step', 'conversion2step', 'conversion3step', 'conversion4step', 'conversion5step'
        // 단계별 전환
        this.tabMove(8)
      }
    },

    //타겟만들기 카테고리 탭
    tabMove (activeNumber, beforeNumber) {
      let tabArray = ['tabActive1','tabActive2','tabActive3','tabActive4','tabActive5','tabActive6','tabActive7','tabActive8','tabActive9']
      let pageNum = (activeNumber == 0) ? '1':'2'

      document.getElementById('page-number').innerText = pageNum

      for(let i = 0; i < tabArray.length; i++) {
        if(i == activeNumber) {
          this.tabAction[tabArray[i]].show = true
        }else{
          this.tabAction[tabArray[i]].show = false
        }
      }
    }
  }
}
</script>

<style lang="css" scoped>
</style>
