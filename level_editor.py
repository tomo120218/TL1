import bpy
import math
import bpy_extras
bl_info = {
    "name": "レベルエディタ",
    "author": "rikuri isobe",
    "version": (1,0),
    "blender": (3,3,21),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object",
}
    
#オペレーター
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    bl_options = {'REGISTER','UNDO'}
    
    def execute(self,context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました。")
        
        return{'FINISHED'}
        
#オペレータICO球生成 
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    bl_options = {'REGISTER','UNDO'}
     
    def execute(self,context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました")
        
        return{'FINISHED'} 
    
#オペレータシーン出力
class MYADDON_OT_export_scene(bpy.types.Operator,bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"
    #出力するファイルの拡張子

    filename_ext=".scene"

    def write_and_print(self,file,str):
        print(str)

        file.write(str)
        file.write('\n')

    def parse_scene_recursive(self,file,object,level):
        """シーン解析用再起関数"""

        # 深さ文インデントする(タブを挿入)

        indent=''
        for i in range(level):
            indent += "\t"

        #オブジェクト名書き込み

        self.write_and_print(file,indent + object.type + " - " + object.name)
        #ローカルトランスフォーム行列から平行移動、回転、スケーリングを抽出

        #型はVector,Quternion,Vector

        trans,rot,scale=object.matrix_local.decompose()
        #回転をQuternionからEuler(三軸での回転角)に変換

        rot=rot.to_euler()
        #ラジアンから度数法に変換

        rot.x=math.degrees(rot.x)
        rot.y=math.degrees(rot.y)
        rot.z=math.degrees(rot.z)
        #トランスフォーム情報を表示

        self.write_and_print(file,indent + "Trans(%f,%f,%f)"%(trans.x,trans.y,trans.z))
        self.write_and_print(file,indent + "Rot(%f,%f,%f)"%(rot.x,rot.y,rot.z))
        self.write_and_print(file,indent + "Scale(%f,%f,%f)"%(scale.x,scale.y,scale.z))
        self.write_and_print(file,'')

        #子ノードへ進む(深さが1上がる)

        for child in object.children:
            self.parse_scene_recursive(file,child,level + 1)

    def export(self):
        """ファイルに出力"""

        print("シーン情報出力開始...%r" % self.filepath)
        
        #ファイルをテキスト形式で書き出し様にオープン

        #スコープを抜けると自動的にクローズされる

        with open(self.filepath,"wt") as file:

            #ファイルに文字列を書き込む

            file.write("SCENE\n")

            #シーン内の全オブジェクトについて

            for object in bpy.context.scene.objects:
                #親オブジェクトがあるものはスキップ(代わりに親から呼び出すから)

                if(object.parent):
                    continue
                
                #シーン直下のオブジェクトをルートノード(深さ0)とし、再起関数で走査

                self.parse_scene_recursive(file,object,0)

    def execute(self,context):
        
        print("シーン情報をExportします")

        #ファイルに出力

        self.export()

        print("シーン情報をExportしました")

        self.report({'INFO'},"シーン情報をExportしました")

        return{'FINISHED'}
    
#トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "MyMenu"
    bl_description = "拡張メニュー by " + bl_info["author"]
    
    #サブメニューの描画
    def draw(self,context):
        self.layout.operator("wm.url_open_preset",
        text="Manual",icon='HELP')
        
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,
        text=MYADDON_OT_stretch_vertex.bl_label)
        
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname, 
        text=MYADDON_OT_create_ico_sphere.bl_label)
        
        self.layout.operator(MYADDON_OT_export_scene.bl_idname, 
        text=MYADDON_OT_export_scene.bl_label)
        
    def submenu(self,context):
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)
    
#Blanderに登録するクラス
classes = (
MYADDON_OT_stretch_vertex,
MYADDON_OT_create_ico_sphere,
MYADDON_OT_export_scene,
TOPBAR_MT_my_menu,
)
    
def draw_meau_manual(self,context):
    self.layout.operator("wm.url_open_preset",text="Manual",icon='HELP')
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    print("レベルエディタが有効化されました。")

def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("レベルエディタが無効化されました。")