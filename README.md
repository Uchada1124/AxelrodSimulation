# AxelrodSimulation

## 概要
URL : <https://axelrodsimulation.streamlit.app/>

Axelrodの繰り返し囚人のジレンマゲームのシミュレーションを実装した. 

### 戦略タイプ
- 悪人戦略[ALLD]
  常に非協力(D)を選ぶ. 
- 善人戦略[ALLC]
  常に協力(C)を選ぶ. 
- しっぺ返し戦略[Tit-For-Tat(TFT)]
  初回は協力を選び, 相手が協力すれば協力(C)を次回選び, 相手が非協力なら非協力(D)を次回選ぶ. 
- 堪忍袋戦略[Tit-For-Two-Tats(TTT)]
  初回は協力(C)を選び, 相手が２回連続で非協力を選んだとき, 非協力(D)を次回選ぶ. 
- Pavlov戦略(PVL)
  初回はC, 二回目以降は, 前回が（C,C）→C, 前回が（C,D）→D, 前回が（D,C）→D, 前回が（D,D）→C. 

### シミュレーション
