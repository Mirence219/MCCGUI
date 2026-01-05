# MCC适配MCCGUI的修改补丁

- 补丁文件：mcc_modifications.patch
- 基于的MCC原始版本：Commit ID `f785f50`（MCC官方仓库的该提交）
- MCC官方仓库地址： https://github.com/MCCTeam/Minecraft-Console-Client
- 应用方法：      
  1. 从MCC官方仓库克隆代码，切换到Commit `f785f50`：
  
	  `git clone https://github.com/MCCTeam/Minecraft-Console-Client`

      `cd Minecraft-Console-Client`
  
      `git checkout f785f50`
  2. 把补丁复制到MCC代码目录；
  3. 执行 `git apply mcc_modifications.patch` 即可应用我的修改。
- 许可证：本补丁及应用补丁后的MCC修改代码均基于CDDL-1.0授权


# MCC Modification Patch for MCCGUI Compatibility
- Patch File: mcc_modifications.patch
- Base MCC Original Version: Commit ID `f785f50` (from the official MCC repository)
- Official MCC Repository: https://github.com/MCCTeam/Minecraft-Console-Client 
- Application Instructions:
  1. Clone the code from the official MCC repository, then switch to Commit `f785f50`：

      `git clone https://github.com/MCCTeam/Minecraft-Console-Client`

      `cd Minecraft-Console-Client`

      `git checkout f785f50`
  2. Copy the patch file to the root directory of the MCC code;
  3. Execute git apply mcc_modifications.patch to apply my changes.
- License: This patch (and the modified MCC code after applying this patch) is licensed under the CDDL-1.0 license.