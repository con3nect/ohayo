<script setup>
    import  {onMounted,ref,onBeforeUnmount}  from "vue"
    import G6 from "@antv/g6";
    const graph = ref(null); // 使用ref存储graph实例

    // 初始化图表
    const initGraph = (data) => {
      const container = document.getElementById('container');
      const width = container.scrollWidth;
      const height = container.scrollHeight || 500;
      graph.value = new G6.TreeGraph({
        container: 'container',
        width,
        height,
        modes: {
          default: [
            {
              type: 'collapse-expand',
              onChange: function onChange(item, collapsed) {
                const data = item.get('model');
                data.collapsed = collapsed;
                return true;
              },
            },
            'drag-canvas',
            'zoom-canvas',
          ],
        },
        defaultNode: {
          size: 26,
          anchorPoints: [
            [0, 0.5],
            [1, 0.5],
          ],
          type: 'rect'
        },
        defaultEdge: {
          type: 'cubic-horizontal',
        },
        layout: {
          type: 'dendrogram',
          direction: 'LR', // H / V / LR / RL / TB / BT
          nodeSep: 30,
          rankSep: 100,
        },
      });

      graph.value.node(function (node) {
        return {
          size: [72, 22],
          label: node.tagName,
          labelCfg: {
            position: 'center',
            offset: 5,
            style: {
              // fill: '#535D79',
              fontSize: 4
            }
          },
          style: {
            fill: node.attrs.fill,
          },
        };
      });

      graph.value.data(data);
      graph.value.render();
      graph.value.fitView();
    };

// 更新图表数据但不重置用户的交互操作
const updateGraphData = async () => {
  try {
    const response = await fetch('http://localhost:8000/get_tree_data');
    if (!response.ok) {
      throw new Error('Network response was not ok: ' + response.statusText);
    }
    const newData = await response.json();
    if (graph.value) {
      // Get current node positions
      const currentData = graph.value.save();
      const nodePositions = {};
      currentData.nodes.forEach(node => {
        nodePositions[node.id] = {
          x: node.x,
          y: node.y,
        };
      });

      // Change data
      graph.value.changeData(newData);

      // Apply the old positions to the new nodes
      const newNodes = graph.value.getNodes();
      newNodes.forEach((node) => {
        const model = node.getModel();
        if (nodePositions[model.id]) {
          graph.value.updateItem(node, {
            x: nodePositions[model.id].x,
            y: nodePositions[model.id].y
          });
        }
      });

      graph.value.refreshPositions(); // Refresh the positions of the nodes
      graph.value.fitView(); // Fit the graph to the view after updating the nodes
    }
  } catch (error) {
    console.error('Failed to load tree data:', error);
  }
};
      
onMounted(async () => {
  // 首次获取数据并初始化图表
  const initialDataResponse = await fetch('http://localhost:8000/get_tree_data');
  if (initialDataResponse.ok) {
    const initialData = await initialDataResponse.json();
    initGraph(initialData); // 调用 initGraph 函数以初始化图表

    // 设置轮询，每2秒更新数据
    const intervalId = setInterval(updateGraphData, 2000);

    // 清除interval
    onBeforeUnmount(() => {
      clearInterval(intervalId);
    });
  } else {
    console.error('Failed to load initial tree data:', initialDataResponse.statusText);
  }

  // 窗口大小变化时重新设置图表大小
  window.onresize = () => {
    if (graph.value && !graph.value.get('destroyed')) {
      const container = document.getElementById('container');
      if (container && container.scrollWidth && container.scrollHeight) {
        graph.value.changeSize(container.scrollWidth, container.scrollHeight);
      }
    }
  };
});

</script>



<script>
import { ElForm, ElInput, ElButton } from 'element-plus';

export default {
  components: {
    ElForm,
    ElInput,
    ElButton
  },
  data() {
    return {
      sendQuestion: ''
    };
  },
  methods: {
    inputFuc() {
      console.log(this.sendQuestion);
    },
    handleSearch() {
      this.submitQuestion(this.sendQuestion);
    },
    submitQuestion(question) {
      // 修改为你的后端接口地址
      const apiUrl = 'http://localhost:8000/submit_question';

      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question })
      })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
  }
};
</script>

<style scoped>
.app-container {
  padding: 20px 20px 20px;
}

.page-card {
  padding: 20px;
}
</style>


<template>
  <div class="flex-col page">
    <div class="flex-col section">
      <div class="flex-col">
        <span class="self-start text">Hi!!</span>
        <br>
        <br>
        <span class="font">我是小法，您的私人法律助手。</span>
      </div>
    </div>
      
  <div class="app-container" style="padding: 20px 20px 20px;">
    <div class="page-card">
      <el-form ref="queryForm" :inline="true" label-width="90px" style="padding-left: 5px;">
        <div style="display: flex; flex-wrap: nowrap; align-items: baseline;">
          <div style="display: flex; align-items: center;">
            <el-form-item label="">
              <el-input v-model="sendQuestion" placeholder=" 请输入想要咨询的法律问题 " clearable maxlength="200" @input="inputFuc" style="width: 1200px; height: 60px;" />
              <el-button style="margin-left: 10px; background-color: #B0C4DE; font-weight: bold; width: 80px; height: 40px;" @click="handleSearch">问问小法</el-button>
            </el-form-item>
          </div>
        </div>
      </el-form>
    </div>
  </div>
  
  <div class="flex-row">
  <div class="flex-col section_2 left-section">
    <span class="font_2">问题处理过程：</span>
    <div id="container"></div>
  </div>
  <div class="flex-col section_3 right-section">
    <span class="font_2 text_3">具体分析如下：</span>
    <br>
    <br>
    <span class="text_4 mt-35">{{ analysisText }}</span>
  </div>
</div>

  </div>
</template>


<style scoped lang="css">
  .mt-73 { margin-top: 4.56rem; }
   .mt-35 { margin-top: 2.19rem; }
   .page {
    padding-bottom: 6.44rem;
    background-image: url(https://codefun-proj-user-res-1256085488.cos.ap-guangzhou.myqcloud.com/655df3d35a7e3f03103ffbfd/655e13d1fcfbac00113472ad/17006643136069374199.png);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    height: 100%;
  }
  .section {
    padding: 8.19rem 11.88rem 3.56rem;
    background-color: #1c1e5380;
  }
  .text {
    margin-left: 0.13rem;
    color: #ffffff;
    font-size: 3.75rem;
    font-family: Poppins;
    font-weight: 600;
    line-height: 2.96rem;
  }
  .font-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  }

  .font {
    font-size: 2.81rem;
    font-family: Poppins;
    line-height: 2.81rem;
    font-weight: 600;
    color: #ffffff;
  }
  .text_2 {
    color: #ffffff;
    font-size: 1.5rem;
    font-family: fangZhengHeiTiJianTi;
    line-height: 1.38rem;
    letter-spacing: -0.078rem;
    text-decoration: underline;
  }
  .section_2 {
    padding: 2.56rem 2.53rem 15rem;
    background-color: #adaec466;
  }
  .font_2 {
    font-size: 1.63rem;
    font-family: fangZhengHeiTiJianTi;
    letter-spacing: -0.078rem;
    line-height: 1.5rem;
    color: #ffffff;
  }
  .image {
    width: 44.41rem;
    height: 18.06rem;
  }
  .section_3 {
    padding: 3.19rem 2.63rem 15rem;
    background-color: #1c1e5380;
  }
  .text_3 {
    line-height: 1.49rem;
  }
  .text_4 {
  margin-left: 2.44rem;
  color: #ffffff;
  font-size: 1.35rem;
  font-family: SourceHanSansCN;
  font-weight: normal;
  line-height: 2rem;
  }

  .flex-row {
    display: flex;
  }

  .flex-col {
    display: flex;
    flex-direction: column;
  }


  .left-section {
    width: 50%;
  }

  .right-section {
    width: 50%;
  }
</style>