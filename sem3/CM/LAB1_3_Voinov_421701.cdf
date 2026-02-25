(* Content-type: application/vnd.wolfram.cdf.text *)

(*** Wolfram CDF File ***)
(* http://www.wolfram.com/cdf *)

(* CreatedBy='Wolfram 14.2' *)

(***************************************************************************)
(*                                                                         *)
(*                                                                         *)
(*  Under the Wolfram FreeCDF terms of use, this file and its content are  *)
(*  bound by the Creative Commons BY-SA Attribution-ShareAlike license.    *)
(*                                                                         *)
(*        For additional information concerning CDF licensing, see:        *)
(*                                                                         *)
(*         www.wolfram.com/cdf/adopting-cdf/licensing-options.html         *)
(*                                                                         *)
(*                                                                         *)
(***************************************************************************)

(*CacheID: 234*)
(* Internal cache information:
NotebookFileLineBreakTest
NotebookFileLineBreakTest
NotebookDataPosition[      1084,         20]
NotebookDataLength[     27829,        730]
NotebookOptionsPosition[     26100,        692]
NotebookOutlinePosition[     26562,        710]
CellTagsIndexPosition[     26519,        707]
WindowFrame->Normal*)

(* Beginning of Notebook Content *)
Notebook[{

Cell[CellGroupData[{
Cell["\:0417\:0430\:0434\:0430\:043d\:0438\:0435 3", "Title",
 CellChangeTimes->{{3.906965784109256*^9, 
  3.9069657906726203`*^9}},ExpressionUUID->"b67fdb47-82d9-45e3-835d-\
f7f72fd1ad87"],

Cell["", "Subtitle",
 CellChangeTimes->{{3.9069657975572968`*^9, 3.9069658131496286`*^9}, 
   3.969554032610594*^9},ExpressionUUID->"1d9e1395-7446-45bf-9e11-\
5937f8898a07"],

Cell[BoxData[{
 RowBox[{
  RowBox[{"\[CurlyEpsilon]", " ", "=", " ", "0.001"}], ";"}], "\[IndentingNewLine]", 
 RowBox[{
  RowBox[{"n", " ", "=", " ", "10"}], ";"}], "\[IndentingNewLine]", 
 RowBox[{
  RowBox[{"k", " ", "=", " ", "9"}], ";"}], "\[IndentingNewLine]", 
 RowBox[{
  RowBox[{"A", " ", "=", " ", 
   RowBox[{"Table", "[", 
    RowBox[{
     RowBox[{"If", "[", 
      RowBox[{
       RowBox[{"i", "!=", "j"}], ",", "1", ",", 
       RowBox[{"2", "n"}]}], "]"}], ",", 
     RowBox[{"{", 
      RowBox[{"i", ",", "1", ",", "n", ",", "1"}], "}"}], ",", " ", 
     RowBox[{"{", 
      RowBox[{"j", ",", "1", ",", "n", ",", "1"}], "}"}]}], "]"}]}], ";"}], "\[IndentingNewLine]", 
 RowBox[{
  RowBox[{"B", "=", 
   RowBox[{"Table", "[", 
    RowBox[{
     RowBox[{
      RowBox[{
       RowBox[{"(", 
        RowBox[{
         RowBox[{"2", "n"}], "-", "1"}], ")"}], "i"}], "+", 
      FractionBox[
       RowBox[{"n", 
        RowBox[{"(", 
         RowBox[{"n", "+", "1"}], ")"}]}], "2"], "+", 
      RowBox[{
       RowBox[{"(", 
        RowBox[{
         RowBox[{"3", "n"}], "-", "1"}], ")"}], 
       RowBox[{"(", 
        RowBox[{"k", "-", "1"}], ")"}]}]}], ",", " ", 
     RowBox[{"{", 
      RowBox[{"i", ",", " ", "1", ",", "n", ",", "1"}], "}"}]}], "]"}]}], 
  ";"}]}], "Input",
 CellChangeTimes->{{3.906965877730585*^9, 3.9069660030950117`*^9}, 
   3.9069660360609426`*^9, {3.906966073086306*^9, 3.906966268087475*^9}, {
   3.9069663102030745`*^9, 3.9069663600035057`*^9}, {3.9069664676429734`*^9, 
   3.9069664884651337`*^9}, {3.906966765829076*^9, 3.9069668470310097`*^9}, {
   3.906966879862426*^9, 3.9069670117688327`*^9}, {3.9069670581549883`*^9, 
   3.90696709834268*^9}, {3.906967148688075*^9, 3.9069673332315903`*^9}, {
   3.906967369437995*^9, 3.9069674300064526`*^9}, {3.906967480496668*^9, 
   3.906967829490001*^9}, {3.9069679187095456`*^9, 3.906968007955031*^9}, {
   3.9069680647349157`*^9, 3.906968146601405*^9}, 3.9069685184841485`*^9, {
   3.906969277883738*^9, 3.9069692866618195`*^9}, {3.9720070816467686`*^9, 
   3.9720070854428444`*^9}, {3.972007206649952*^9, 
   3.9720072173702183`*^9}},ExpressionUUID->"40ed09f4-50d2-47eb-96fb-\
ab61723a3d3a"],

Cell[BoxData[
 RowBox[{
  RowBox[{
   RowBox[{"S", "[", 
    RowBox[{"i_", ",", " ", "X_"}], "]"}], ":=", 
   RowBox[{"Module", "[", 
    RowBox[{
     RowBox[{"{", 
      RowBox[{"S", "=", "0"}], "}"}], ",", "\[IndentingNewLine]", 
     RowBox[{
      RowBox[{"For", "[", 
       RowBox[{
        RowBox[{"j", "=", "1"}], ",", 
        RowBox[{"j", "<", "n"}], ",", " ", 
        RowBox[{"j", "++"}], ",", " ", 
        RowBox[{"If", "[", 
         RowBox[{
          RowBox[{"j", "!=", "i"}], ",", 
          RowBox[{"S", "=", 
           RowBox[{"S", "+", 
            RowBox[{
             RowBox[{
              RowBox[{"A", "[", 
               RowBox[{"[", "i", "]"}], "]"}], "[", 
              RowBox[{"[", "j", "]"}], "]"}], 
             RowBox[{"X", "[", 
              RowBox[{"[", "j", "]"}], "]"}]}], "-", 
            RowBox[{"B", "[", 
             RowBox[{"[", "i", "]"}], "]"}]}]}]}], "]"}]}], "]"}], ";", 
      "\[IndentingNewLine]", "S"}]}], "\[IndentingNewLine]", "]"}]}], 
  ";"}]], "Input",
 CellChangeTimes->{{3.906965877730585*^9, 3.9069660030950117`*^9}, 
   3.9069660360609426`*^9, {3.906966073086306*^9, 3.906966268087475*^9}, {
   3.9069663102030745`*^9, 3.9069663600035057`*^9}, {3.9069664676429734`*^9, 
   3.9069664884651337`*^9}, {3.906966765829076*^9, 3.9069668470310097`*^9}, {
   3.906966879862426*^9, 3.9069670117688327`*^9}, {3.9069670581549883`*^9, 
   3.90696709834268*^9}, {3.906967148688075*^9, 3.9069673332315903`*^9}, {
   3.906967369437995*^9, 3.9069674300064526`*^9}, {3.906967480496668*^9, 
   3.906967829490001*^9}, {3.9069679187095456`*^9, 3.906968007955031*^9}, {
   3.9069680647349157`*^9, 3.906968146601405*^9}, 3.9069685184841485`*^9, 
   3.906968635916684*^9, {3.9069687678690042`*^9, 3.9069687698326254`*^9}, 
   3.906968815887385*^9, {3.906968849345058*^9, 3.9069688558897486`*^9}, {
   3.906968895916847*^9, 3.9069689029232397`*^9}},
 CellLabel->"In[9]:=",ExpressionUUID->"9271a89c-60c6-4597-89b7-ec1c61fbcac0"],

Cell[CellGroupData[{

Cell["\:042f\:043a\:043e\:0431\:0438", "Section",
 CellChangeTimes->{{3.906968158282202*^9, 
  3.9069681631249876`*^9}},ExpressionUUID->"2896bbcf-7548-4f48-b86b-\
3d8028f5c24e"],

Cell[BoxData[
 RowBox[{
  RowBox[{
   RowBox[{"J", "[", "X0_", "]"}], " ", ":=", " ", 
   RowBox[{"Module", "[", 
    RowBox[{
     RowBox[{"{", 
      RowBox[{
       RowBox[{"X", "=", "X0"}], ",", 
       RowBox[{"e", "=", 
        RowBox[{"\[CurlyEpsilon]", "+", "1"}]}], ",", 
       RowBox[{"k", "=", "0"}]}], "}"}], ",", "\[IndentingNewLine]", 
     RowBox[{
      RowBox[{"While", "[", 
       RowBox[{
        RowBox[{"e", " ", ">", " ", "\[CurlyEpsilon]"}], ",", 
        "\[IndentingNewLine]", 
        RowBox[{
         RowBox[{"If", "[", 
          RowBox[{
           RowBox[{
            RowBox[{"k", "~", "Mod", "~", "10"}], " ", "==", "0"}], ",", 
           "\[IndentingNewLine]", 
           RowBox[{
            RowBox[{"Print", "[", 
             RowBox[{"\"\<k = \>\"", ",", " ", "k"}], "]"}], ";", 
            "\[IndentingNewLine]", 
            RowBox[{"Print", "[", 
             RowBox[{"\"\<X = \>\"", ",", " ", 
              RowBox[{
               RowBox[{"Table", "[", 
                RowBox[{
                 RowBox[{
                  RowBox[{"X", "[", 
                   RowBox[{"[", "i", "]"}], "]"}], "//", "N"}], ",", " ", 
                 RowBox[{"{", 
                  RowBox[{"i", ",", "1", ",", "n", ",", "1"}], "}"}]}], "]"}],
                " ", "//", "MatrixForm"}]}], "]"}]}]}], "\[IndentingNewLine]",
           "]"}], ";", "\[IndentingNewLine]", 
         RowBox[{"Xp", "=", "X"}], ";", "\[IndentingNewLine]", 
         RowBox[{"X", "=", 
          RowBox[{"Table", "[", 
           RowBox[{
            FractionBox[
             RowBox[{
              RowBox[{"B", "[", 
               RowBox[{"[", "i", "]"}], "]"}], " ", "-", " ", 
              RowBox[{"Sum", "[", 
               RowBox[{
                RowBox[{"If", "[", 
                 RowBox[{
                  RowBox[{"j", "!=", "i"}], ",", 
                  RowBox[{
                   RowBox[{
                    RowBox[{"A", "[", 
                    RowBox[{"[", "i", "]"}], "]"}], "[", 
                    RowBox[{"[", "j", "]"}], "]"}], 
                   RowBox[{"Xp", "[", 
                    RowBox[{"[", "j", "]"}], "]"}]}], ",", " ", "0"}], "]"}], 
                ",", 
                RowBox[{"{", 
                 RowBox[{"j", ",", "1", ",", "n", ",", "1"}], "}"}]}], 
               "]"}]}], 
             RowBox[{
              RowBox[{"A", "[", 
               RowBox[{"[", "i", "]"}], "]"}], "[", 
              RowBox[{"[", "i", "]"}], "]"}]], ",", 
            RowBox[{"{", 
             RowBox[{"i", ",", "1", ",", "n", ",", "1"}], "}"}]}], "]"}]}], ";",
          "\[IndentingNewLine]", 
         RowBox[{"k", "++"}], ";", "\[IndentingNewLine]", 
         RowBox[{"e", "=", 
          RowBox[{"Max", "[", 
           RowBox[{"Abs", "[", 
            RowBox[{"X", " ", "-", " ", "Xp"}], "]"}], "]"}]}], ";"}]}], 
       "\[IndentingNewLine]", "]"}], " ", ";", "\[IndentingNewLine]", 
      RowBox[{"{", 
       RowBox[{
        RowBox[{"Table", "[", 
         RowBox[{
          RowBox[{
           RowBox[{"X", "[", 
            RowBox[{"[", "i", "]"}], "]"}], "//", "N"}], ",", " ", 
          RowBox[{"{", 
           RowBox[{"i", ",", "1", ",", "n", ",", "1"}], "}"}]}], "]"}], ",", 
        " ", "k"}], "}"}]}]}], "\[IndentingNewLine]", "]"}]}], ";"}]], "Input",
 CellChangeTimes->{{3.906965877730585*^9, 3.9069660030950117`*^9}, 
   3.9069660360609426`*^9, {3.906966073086306*^9, 3.906966268087475*^9}, {
   3.9069663102030745`*^9, 3.9069663600035057`*^9}, {3.9069664676429734`*^9, 
   3.9069664884651337`*^9}, {3.906966765829076*^9, 3.9069668470310097`*^9}, {
   3.906966879862426*^9, 3.9069670117688327`*^9}, {3.9069670581549883`*^9, 
   3.90696709834268*^9}, {3.906967148688075*^9, 3.9069673332315903`*^9}, {
   3.906967369437995*^9, 3.9069674300064526`*^9}, {3.906967480496668*^9, 
   3.906967829490001*^9}, {3.9069679187095456`*^9, 3.906968007955031*^9}, {
   3.9069680647349157`*^9, 3.906968146601405*^9}, {3.906968177458514*^9, 
   3.9069684199991617`*^9}, {3.906969250044262*^9, 3.9069692503607864`*^9}, {
   3.9069693080854387`*^9, 3.9069693090511074`*^9}, {3.9069693590597353`*^9, 
   3.9069694471944323`*^9}, {3.9069738223097925`*^9, 3.906973839401665*^9}, {
   3.906973880445838*^9, 3.9069739715388803`*^9}},
 CellLabel->"In[10]:=",ExpressionUUID->"e93c0ffd-f662-45fe-8b6a-2ba5b92cd84f"],

Cell[CellGroupData[{

Cell[BoxData[{
 RowBox[{
  RowBox[{
   RowBox[{"{", 
    RowBox[{"Xj", ",", "kj"}], "}"}], " ", "=", " ", 
   RowBox[{"J", "[", 
    RowBox[{"Table", "[", 
     RowBox[{"0", ",", 
      RowBox[{"{", 
       RowBox[{"i", ",", "1", ",", "n", ",", "1"}], "}"}]}], "]"}], "]"}]}], 
  ";"}], "\[IndentingNewLine]", "kj", "\[IndentingNewLine]", 
 RowBox[{"Xj", " ", "//", " ", "MatrixForm"}]}], "Input",
 CellChangeTimes->{{3.9069696324026017`*^9, 3.906969712367089*^9}, 
   3.906973484744396*^9},
 CellLabel->"In[11]:=",ExpressionUUID->"a9fcd40f-4c33-450b-8f72-4cf5e7e758b2"],

Cell[CellGroupData[{

Cell[BoxData[
 InterpretationBox[
  RowBox[{"\<\"k = \"\>", "\[InvisibleSpace]", "0"}],
  SequenceForm["k = ", 0],
  Editable->False]], "Print",
 CellChangeTimes->{{3.906969664539767*^9, 3.9069696754262524`*^9}, 
   3.90696971333018*^9, 3.9069734860268373`*^9, {3.9069738458710384`*^9, 
   3.906973860044403*^9}, {3.906973900968758*^9, 3.906973923020295*^9}, {
   3.906973974680376*^9, 3.906973986954422*^9}, 3.9069829601684933`*^9},
 CellLabel->
  "During evaluation of \
In[11]:=",ExpressionUUID->"07c5da21-ec88-446d-bccb-29a787f99ec8"],

Cell[BoxData[
 InterpretationBox[
  RowBox[{"\<\"X = \"\>", "\[InvisibleSpace]", 
   TagBox[
    RowBox[{"(", "\[NoBreak]", 
     TagBox[GridBox[{
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"}
       },
       GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
       GridBoxSpacings->{"Columns" -> {
           Offset[0.27999999999999997`], {
            Offset[0.5599999999999999]}, 
           Offset[0.27999999999999997`]}, "Rows" -> {
           Offset[0.2], {
            Offset[0.4]}, 
           Offset[0.2]}}],
      Column], "\[NoBreak]", ")"}],
    Function[BoxForm`e$, 
     MatrixForm[BoxForm`e$]]]}],
  SequenceForm["X = ", 
   MatrixForm[{0., 0., 0., 0., 0., 0., 0., 0., 0., 0.}]],
  Editable->False]], "Print",
 CellChangeTimes->{{3.906969664539767*^9, 3.9069696754262524`*^9}, 
   3.90696971333018*^9, 3.9069734860268373`*^9, {3.9069738458710384`*^9, 
   3.906973860044403*^9}, {3.906973900968758*^9, 3.906973923020295*^9}, {
   3.906973974680376*^9, 3.906973986954422*^9}, 3.9069829601775107`*^9},
 CellLabel->
  "During evaluation of \
In[11]:=",ExpressionUUID->"4d7776f8-57b2-4f33-8e9c-41048b2a3578"],

Cell[BoxData[
 InterpretationBox[
  RowBox[{"\<\"k = \"\>", "\[InvisibleSpace]", "10"}],
  SequenceForm["k = ", 10],
  Editable->False]], "Print",
 CellChangeTimes->{{3.906969664539767*^9, 3.9069696754262524`*^9}, 
   3.90696971333018*^9, 3.9069734860268373`*^9, {3.9069738458710384`*^9, 
   3.906973860044403*^9}, {3.906973900968758*^9, 3.906973923020295*^9}, {
   3.906973974680376*^9, 3.906973986954422*^9}, 3.9069829601775107`*^9},
 CellLabel->
  "During evaluation of \
In[11]:=",ExpressionUUID->"8426a3ea-bc7d-4996-acb4-b0f75e980ab7"],

Cell[BoxData[
 InterpretationBox[
  RowBox[{"\<\"X = \"\>", "\[InvisibleSpace]", 
   TagBox[
    RowBox[{"(", "\[NoBreak]", 
     TagBox[GridBox[{
        {"0.9981272154100586`"},
        {"1.998127215409961`"},
        {"2.9981272154098635`"},
        {"3.998127215409766`"},
        {"4.998127215409668`"},
        {"5.99812721540957`"},
        {"6.998127215409473`"},
        {"7.998127215409375`"},
        {"8.998127215409278`"},
        {"9.99812721540918`"}
       },
       GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
       GridBoxSpacings->{"Columns" -> {
           Offset[0.27999999999999997`], {
            Offset[0.5599999999999999]}, 
           Offset[0.27999999999999997`]}, "Rows" -> {
           Offset[0.2], {
            Offset[0.4]}, 
           Offset[0.2]}}],
      Column], "\[NoBreak]", ")"}],
    Function[BoxForm`e$, 
     MatrixForm[BoxForm`e$]]]}],
  SequenceForm["X = ", 
   MatrixForm[{0.9981272154100586, 1.998127215409961, 2.9981272154098635`, 
    3.998127215409766, 4.998127215409668, 5.99812721540957, 6.998127215409473,
     7.998127215409375, 8.998127215409278, 9.99812721540918}]],
  Editable->False]], "Print",
 CellChangeTimes->{{3.906969664539767*^9, 3.9069696754262524`*^9}, 
   3.90696971333018*^9, 3.9069734860268373`*^9, {3.9069738458710384`*^9, 
   3.906973860044403*^9}, {3.906973900968758*^9, 3.906973923020295*^9}, {
   3.906973974680376*^9, 3.906973986954422*^9}, 3.9069829601775107`*^9},
 CellLabel->
  "During evaluation of \
In[11]:=",ExpressionUUID->"f30af5d8-134c-44b8-b64e-5166decfe0ee"]
}, Open  ]],

Cell[BoxData["13"], "Output",
 CellChangeTimes->{
  3.90696967544188*^9, 3.9069697133523617`*^9, 3.9069734860490265`*^9, {
   3.9069738459372454`*^9, 3.906973860060027*^9}, {3.906973900975314*^9, 
   3.906973923035901*^9}, {3.906973974680376*^9, 3.906973986976622*^9}, 
   3.9069829601775107`*^9},
 CellLabel->"Out[12]=",ExpressionUUID->"fa9df956-c3c4-4097-be20-ee73ac5aba22"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", 
   TagBox[GridBox[{
      {"1.0001706574957985`"},
      {"2.0001706574957985`"},
      {"3.0001706574957985`"},
      {"4.000170657495798`"},
      {"5.000170657495799`"},
      {"6.000170657495798`"},
      {"7.000170657495798`"},
      {"8.000170657495799`"},
      {"9.000170657495799`"},
      {"10.000170657495799`"}
     },
     GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
     GridBoxSpacings->{"Columns" -> {
         Offset[0.27999999999999997`], {
          Offset[0.5599999999999999]}, 
         Offset[0.27999999999999997`]}, "Rows" -> {
         Offset[0.2], {
          Offset[0.4]}, 
         Offset[0.2]}}],
    Column], "\[NoBreak]", ")"}],
  Function[BoxForm`e$, 
   MatrixForm[BoxForm`e$]]]], "Output",
 CellFrame->{{1, 1}, {1, 1}},
 CellChangeTimes->{
  3.90696967544188*^9, 3.9069697133523617`*^9, 3.9069734860490265`*^9, {
   3.9069738459372454`*^9, 3.906973860060027*^9}, {3.906973900975314*^9, 
   3.906973923035901*^9}, {3.906973974680376*^9, 3.906973986976622*^9}, 
   3.9069829601931477`*^9},
 Background->RGBColor[0.9, 1, 1],
 CellLabel->
  "Out[13]//MatrixForm=",ExpressionUUID->"b0eb3aa3-587d-48c9-9117-\
4fedf1fcc604"]
}, Open  ]]
}, Open  ]],

Cell[CellGroupData[{

Cell["\:0417\:0435\:0439\:0434\:0435\:043b\:044c", "Section",
 CellChangeTimes->{{3.9069695199902153`*^9, 
  3.9069695234891963`*^9}},ExpressionUUID->"b995af41-bce4-4687-9adf-\
d673bf8889a2"],

Cell[BoxData[
 RowBox[{
  RowBox[{
   RowBox[{"Z", "[", "X0_", "]"}], " ", ":=", " ", 
   RowBox[{"Module", "[", 
    RowBox[{
     RowBox[{"{", 
      RowBox[{
       RowBox[{"X", "=", "X0"}], ",", 
       RowBox[{"e", "=", 
        RowBox[{"\[CurlyEpsilon]", "+", "1"}]}], ",", 
       RowBox[{"k", "=", "0"}]}], "}"}], ",", "\[IndentingNewLine]", 
     RowBox[{
      RowBox[{"While", "[", 
       RowBox[{
        RowBox[{"e", " ", ">", " ", "\[CurlyEpsilon]"}], ",", 
        "\[IndentingNewLine]", 
        RowBox[{
         RowBox[{"If", "[", 
          RowBox[{
           RowBox[{
            RowBox[{"k", "~", "Mod", "~", "10"}], " ", "==", "0"}], ",", 
           "\[IndentingNewLine]", 
           RowBox[{
            RowBox[{"Print", "[", 
             RowBox[{"\"\<k = \>\"", ",", " ", "k"}], "]"}], ";", 
            "\[IndentingNewLine]", 
            RowBox[{"Print", "[", 
             RowBox[{"\"\<X = \>\"", ",", " ", 
              RowBox[{
               RowBox[{"Table", "[", 
                RowBox[{
                 RowBox[{
                  RowBox[{"X", "[", 
                   RowBox[{"[", "i", "]"}], "]"}], "//", "N"}], ",", " ", 
                 RowBox[{"{", 
                  RowBox[{"i", ",", "1", ",", "n", ",", "1"}], "}"}]}], "]"}],
                " ", "//", "MatrixForm"}]}], "]"}]}]}], "\[IndentingNewLine]",
           "]"}], ";", "\[IndentingNewLine]", 
         RowBox[{"Xp", "=", "X"}], ";", "\[IndentingNewLine]", 
         RowBox[{"X", "=", 
          RowBox[{"Table", "[", 
           RowBox[{
            FractionBox[
             RowBox[{
              RowBox[{"B", "[", 
               RowBox[{"[", "i", "]"}], "]"}], "-", 
              RowBox[{"Sum", "[", 
               RowBox[{
                RowBox[{
                 RowBox[{"A", "[", 
                  RowBox[{"[", 
                   RowBox[{"i", ",", "j"}], "]"}], "]"}], "*", 
                 RowBox[{"X", "[", 
                  RowBox[{"[", "j", "]"}], "]"}]}], ",", 
                RowBox[{"{", 
                 RowBox[{"j", ",", "1", ",", 
                  RowBox[{"i", "-", "1"}]}], "}"}]}], "]"}], "-", 
              RowBox[{"Sum", "[", 
               RowBox[{
                RowBox[{
                 RowBox[{"A", "[", 
                  RowBox[{"[", 
                   RowBox[{"i", ",", "j"}], "]"}], "]"}], "*", 
                 RowBox[{"Xp", "[", 
                  RowBox[{"[", "j", "]"}], "]"}]}], ",", 
                RowBox[{"{", 
                 RowBox[{"j", ",", 
                  RowBox[{"i", "+", "1"}], ",", "n"}], "}"}]}], "]"}]}], 
             RowBox[{"A", "[", 
              RowBox[{"[", 
               RowBox[{"i", ",", "i"}], "]"}], "]"}]], ",", 
            RowBox[{"{", 
             RowBox[{"i", ",", "1", ",", "n", ",", "1"}], "}"}]}], "]"}]}], ";",
          "\[IndentingNewLine]", 
         RowBox[{"k", "++"}], ";", "\[IndentingNewLine]", 
         RowBox[{"e", "=", 
          RowBox[{"Max", "[", 
           RowBox[{"Abs", "[", 
            RowBox[{"X", " ", "-", " ", "Xp"}], "]"}], "]"}]}], ";"}]}], 
       "\[IndentingNewLine]", "]"}], " ", ";", "\[IndentingNewLine]", 
      RowBox[{"{", 
       RowBox[{
        RowBox[{"Table", "[", 
         RowBox[{
          RowBox[{
           RowBox[{"X", "[", 
            RowBox[{"[", "i", "]"}], "]"}], "//", "N"}], ",", " ", 
          RowBox[{"{", 
           RowBox[{"i", ",", "1", ",", "n", ",", "1"}], "}"}]}], "]"}], ",", 
        " ", "k"}], "}"}]}]}], "\[IndentingNewLine]", "]"}]}], ";"}]], "Input",
 CellChangeTimes->{{3.906969588787243*^9, 3.9069695908099546`*^9}, {
  3.9069730954923105`*^9, 3.9069730991594763`*^9}, {3.9069735978705063`*^9, 
  3.9069736172876577`*^9}, {3.906973686946948*^9, 3.906973728499738*^9}},
 CellLabel->"In[14]:=",ExpressionUUID->"6a3ff9b9-c291-4d49-950a-456aee5e25f1"],

Cell[CellGroupData[{

Cell[BoxData[{
 RowBox[{
  RowBox[{
   RowBox[{"{", 
    RowBox[{"Xz", ",", " ", "kz"}], "}"}], " ", "=", " ", 
   RowBox[{"Z", "[", 
    RowBox[{"Table", "[", 
     RowBox[{"0", ",", 
      RowBox[{"{", 
       RowBox[{"i", ",", "1", ",", "n", ",", "1"}], "}"}]}], "]"}], "]"}]}], 
  ";"}], "\[IndentingNewLine]", "kz", "\[IndentingNewLine]", 
 RowBox[{"Xz", " ", "//", " ", "MatrixForm"}]}], "Input",
 CellChangeTimes->{{3.906973141134504*^9, 3.9069731657110677`*^9}, {
  3.9069733009133472`*^9, 3.9069733082073936`*^9}, {3.9069733850710735`*^9, 
  3.906973455969966*^9}, {3.906982928539574*^9, 3.906982955039465*^9}},
 CellLabel->"In[15]:=",ExpressionUUID->"27d7e1fb-4688-470f-a28c-d93433e739c1"],

Cell[CellGroupData[{

Cell[BoxData[
 InterpretationBox[
  RowBox[{"\<\"k = \"\>", "\[InvisibleSpace]", "0"}],
  SequenceForm["k = ", 0],
  Editable->False]], "Print",
 CellChangeTimes->{3.9069829602243967`*^9},
 CellLabel->
  "During evaluation of \
In[15]:=",ExpressionUUID->"c20056e9-16f7-4bb8-b000-12cbd18e89d1"],

Cell[BoxData[
 InterpretationBox[
  RowBox[{"\<\"X = \"\>", "\[InvisibleSpace]", 
   TagBox[
    RowBox[{"(", "\[NoBreak]", 
     TagBox[GridBox[{
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"},
        {"0.`"}
       },
       GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
       GridBoxSpacings->{"Columns" -> {
           Offset[0.27999999999999997`], {
            Offset[0.5599999999999999]}, 
           Offset[0.27999999999999997`]}, "Rows" -> {
           Offset[0.2], {
            Offset[0.4]}, 
           Offset[0.2]}}],
      Column], "\[NoBreak]", ")"}],
    Function[BoxForm`e$, 
     MatrixForm[BoxForm`e$]]]}],
  SequenceForm["X = ", 
   MatrixForm[{0., 0., 0., 0., 0., 0., 0., 0., 0., 0.}]],
  Editable->False]], "Print",
 CellChangeTimes->{3.9069829602400274`*^9},
 CellLabel->
  "During evaluation of \
In[15]:=",ExpressionUUID->"9f4bfe4d-c2a4-4155-8fe1-55b561d96002"],

Cell[BoxData[
 InterpretationBox[
  RowBox[{"\<\"k = \"\>", "\[InvisibleSpace]", "10"}],
  SequenceForm["k = ", 10],
  Editable->False]], "Print",
 CellChangeTimes->{3.9069829602400274`*^9},
 CellLabel->
  "During evaluation of \
In[15]:=",ExpressionUUID->"410aa719-0344-432e-a963-20848b706b01"],

Cell[BoxData[
 InterpretationBox[
  RowBox[{"\<\"X = \"\>", "\[InvisibleSpace]", 
   TagBox[
    RowBox[{"(", "\[NoBreak]", 
     TagBox[GridBox[{
        {"0.9981272154100586`"},
        {"1.998127215409961`"},
        {"2.9981272154098635`"},
        {"3.998127215409766`"},
        {"4.998127215409668`"},
        {"5.99812721540957`"},
        {"6.998127215409473`"},
        {"7.998127215409375`"},
        {"8.998127215409278`"},
        {"9.99812721540918`"}
       },
       GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
       GridBoxSpacings->{"Columns" -> {
           Offset[0.27999999999999997`], {
            Offset[0.5599999999999999]}, 
           Offset[0.27999999999999997`]}, "Rows" -> {
           Offset[0.2], {
            Offset[0.4]}, 
           Offset[0.2]}}],
      Column], "\[NoBreak]", ")"}],
    Function[BoxForm`e$, 
     MatrixForm[BoxForm`e$]]]}],
  SequenceForm["X = ", 
   MatrixForm[{0.9981272154100586, 1.998127215409961, 2.9981272154098635`, 
    3.998127215409766, 4.998127215409668, 5.99812721540957, 6.998127215409473,
     7.998127215409375, 8.998127215409278, 9.99812721540918}]],
  Editable->False]], "Print",
 CellChangeTimes->{3.906982960255649*^9},
 CellLabel->
  "During evaluation of \
In[15]:=",ExpressionUUID->"6958a568-9ccc-4e4c-90f3-b3ab9f4f857a"]
}, Open  ]],

Cell[BoxData["13"], "Output",
 CellChangeTimes->{
  3.9069731677761803`*^9, 3.9069732001973*^9, 3.906973308976493*^9, 
   3.906973386708585*^9, {3.9069734278300657`*^9, 3.906973457576024*^9}, 
   3.9069737570657578`*^9, {3.9069829558792343`*^9, 3.906982960255649*^9}},
 CellLabel->"Out[16]=",ExpressionUUID->"7b6401f5-4e5e-4e20-8efe-086adb02ed80"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", 
   TagBox[GridBox[{
      {"1.0001706574957985`"},
      {"2.0001706574957985`"},
      {"3.0001706574957985`"},
      {"4.000170657495798`"},
      {"5.000170657495799`"},
      {"6.000170657495798`"},
      {"7.000170657495798`"},
      {"8.000170657495799`"},
      {"9.000170657495799`"},
      {"10.000170657495799`"}
     },
     GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
     GridBoxSpacings->{"Columns" -> {
         Offset[0.27999999999999997`], {
          Offset[0.5599999999999999]}, 
         Offset[0.27999999999999997`]}, "Rows" -> {
         Offset[0.2], {
          Offset[0.4]}, 
         Offset[0.2]}}],
    Column], "\[NoBreak]", ")"}],
  Function[BoxForm`e$, 
   MatrixForm[BoxForm`e$]]]], "Output",
 CellFrame->{{1, 1}, {1, 1}},
 CellChangeTimes->{
  3.9069731677761803`*^9, 3.9069732001973*^9, 3.906973308976493*^9, 
   3.906973386708585*^9, {3.9069734278300657`*^9, 3.906973457576024*^9}, 
   3.9069737570657578`*^9, {3.9069829558792343`*^9, 3.906982960255649*^9}},
 Background->RGBColor[0.9, 1, 1],
 CellLabel->
  "Out[17]//MatrixForm=",ExpressionUUID->"05120acd-28fe-48e3-9cb2-\
0b7a5f7fc5d8"]
}, Open  ]]
}, Open  ]]
}, Open  ]]
},
WindowSize->{Full, Full},
WindowMargins->{{0, Automatic}, {Automatic, 0}},
TaggingRules-><|"TryRealOnly" -> False|>,
CellContext->Notebook,
FrontEndVersion->"14.3 for Microsoft Windows (64-bit) (July 8, 2025)",
StyleDefinitions->"Default.nb",
ExpressionUUID->"5fac3033-2797-42b0-8022-a40e8f3203a2"
]
(* End of Notebook Content *)

(* Internal cache information *)
(*CellTagsOutline
CellTagsIndex->{}
*)
(*CellTagsIndex
CellTagsIndex->{}
*)
(*NotebookFileOutline
Notebook[{
Cell[CellGroupData[{
Cell[1506, 35, 189, 3, 96, "Title",ExpressionUUID->"b67fdb47-82d9-45e3-835d-f7f72fd1ad87"],
Cell[1698, 40, 173, 3, 52, "Subtitle",ExpressionUUID->"1d9e1395-7446-45bf-9e11-5937f8898a07"],
Cell[1874, 45, 2182, 53, 120, "Input",ExpressionUUID->"40ed09f4-50d2-47eb-96fb-ab61723a3d3a"],
Cell[4059, 100, 1970, 43, 85, "Input",ExpressionUUID->"9271a89c-60c6-4597-89b7-ec1c61fbcac0"],
Cell[CellGroupData[{
Cell[6054, 147, 177, 3, 66, "Section",ExpressionUUID->"2896bbcf-7548-4f48-b86b-3d8028f5c24e"],
Cell[6234, 152, 4349, 99, 311, "Input",ExpressionUUID->"e93c0ffd-f662-45fe-8b6a-2ba5b92cd84f"],
Cell[CellGroupData[{
Cell[10608, 255, 570, 14, 66, "Input",ExpressionUUID->"a9fcd40f-4c33-450b-8f72-4cf5e7e758b2"],
Cell[CellGroupData[{
Cell[11203, 273, 538, 11, 22, "Print",ExpressionUUID->"07c5da21-ec88-446d-bccb-29a787f99ec8"],
Cell[11744, 286, 1261, 37, 158, "Print",ExpressionUUID->"4d7776f8-57b2-4f33-8e9c-41048b2a3578"],
Cell[13008, 325, 540, 11, 22, "Print",ExpressionUUID->"8426a3ea-bc7d-4996-acb4-b0f75e980ab7"],
Cell[13551, 338, 1572, 39, 158, "Print",ExpressionUUID->"f30af5d8-134c-44b8-b64e-5166decfe0ee"]
}, Open  ]],
Cell[15138, 380, 376, 6, 32, "Output",ExpressionUUID->"fa9df956-c3c4-4097-be20-ee73ac5aba22"],
Cell[15517, 388, 1228, 35, 211, "Output",ExpressionUUID->"b0eb3aa3-587d-48c9-9117-4fedf1fcc604"]
}, Open  ]]
}, Open  ]],
Cell[CellGroupData[{
Cell[16794, 429, 191, 3, 66, "Section",ExpressionUUID->"b995af41-bce4-4687-9adf-d673bf8889a2"],
Cell[16988, 434, 3821, 94, 311, "Input",ExpressionUUID->"6a3ff9b9-c291-4d49-950a-456aee5e25f1"],
Cell[CellGroupData[{
Cell[20834, 532, 699, 15, 66, "Input",ExpressionUUID->"27d7e1fb-4688-470f-a28c-d93433e739c1"],
Cell[CellGroupData[{
Cell[21558, 551, 293, 8, 22, "Print",ExpressionUUID->"c20056e9-16f7-4bb8-b000-12cbd18e89d1"],
Cell[21854, 561, 1016, 34, 158, "Print",ExpressionUUID->"9f4bfe4d-c2a4-4155-8fe1-55b561d96002"],
Cell[22873, 597, 295, 8, 22, "Print",ExpressionUUID->"410aa719-0344-432e-a963-20848b706b01"],
Cell[23171, 607, 1325, 36, 158, "Print",ExpressionUUID->"6958a568-9ccc-4e4c-90f3-b3ab9f4f857a"]
}, Open  ]],
Cell[24511, 646, 347, 5, 32, "Output",ExpressionUUID->"7b6401f5-4e5e-4e20-8efe-086adb02ed80"],
Cell[24861, 653, 1199, 34, 211, "Output",ExpressionUUID->"05120acd-28fe-48e3-9cb2-0b7a5f7fc5d8"]
}, Open  ]]
}, Open  ]]
}, Open  ]]
}
]
*)

(* NotebookSignature ZxD6kCIEEVMRyD14Nzmqi@LC *)
