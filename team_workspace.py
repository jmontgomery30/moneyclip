import os
import json

class TeamWorkspace:
    def __init__(self, workspace_name):
        self.workspace_name = workspace_name
        self.members = []
        self.brand_templates = {}
        self.asset_library = {}

    def add_member(self, member_name):
        if member_name not in self.members:
            self.members.append(member_name)
            return f"Member {member_name} added successfully."
        return f"Member {member_name} already exists."

    def remove_member(self, member_name):
        if member_name in self.members:
            self.members.remove(member_name)
            return f"Member {member_name} removed successfully."
        return f"Member {member_name} does not exist."

    def create_brand_template(self, template_name, fonts, logos, colors):
        if template_name not in self.brand_templates:
            self.brand_templates[template_name] = {
                "fonts": fonts,
                "logos": logos,
                "colors": colors
            }
            return f"Brand template {template_name} created successfully."
        return f"Brand template {template_name} already exists."

    def get_brand_template(self, template_name):
        return self.brand_templates.get(template_name, "Brand template not found.")

    def add_asset(self, asset_name, asset_path):
        if asset_name not in self.asset_library:
            self.asset_library[asset_name] = asset_path
            return f"Asset {asset_name} added successfully."
        return f"Asset {asset_name} already exists."

    def get_asset(self, asset_name):
        return self.asset_library.get(asset_name, "Asset not found.")

    def save_workspace(self, file_path):
        workspace_data = {
            "workspace_name": self.workspace_name,
            "members": self.members,
            "brand_templates": self.brand_templates,
            "asset_library": self.asset_library
        }
        with open(file_path, 'w') as file:
            json.dump(workspace_data, file)
        return f"Workspace saved to {file_path}."

    def load_workspace(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                workspace_data = json.load(file)
                self.workspace_name = workspace_data.get("workspace_name", self.workspace_name)
                self.members = workspace_data.get("members", self.members)
                self.brand_templates = workspace_data.get("brand_templates", self.brand_templates)
                self.asset_library = workspace_data.get("asset_library", self.asset_library)
            return f"Workspace loaded from {file_path}."
        return f"Workspace file {file_path} does not exist."
