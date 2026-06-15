import bpy
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
class MYADOON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myadoon.myadoon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    bl_options = {'REGISTER','UNDO'}
     
    def execute(self,context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました")
        
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
        
        self.layout.operator(MYADOON_OT_create_ico_sphere.bl_idname, 
        text=MYADOON_OT_create_ico_sphere.bl_label)
        
    def submenu(self,context):
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)
    
#Blanderに登録するクラス
classes = (
MYADDON_OT_stretch_vertex,
MYADOON_OT_create_ico_sphere,
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