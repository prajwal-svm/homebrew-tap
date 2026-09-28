cask "folderskin" do
  version "0.1.13"
  sha256 "b05d6c5c9cb28e22a8b16790afffcd26aa1107a21a87e862f2b47ccfcba75530"

  url "https://github.com/prajwal-svm/folderskin/releases/download/v#{version}/FolderSkin_#{version}_universal.dmg",
      verified: "github.com/prajwal-svm/folderskin/"
  name "FolderSkin"
  desc "Custom folder and drive icons from art, photos or AI"
  homepage "https://folderskin.app/"

  livecheck do
    url :url
    strategy :github_latest
  end

  auto_updates true
  depends_on macos: ">= :monterey"

  app "FolderSkin.app"

  zap trash: [
    "~/Library/Application Support/app.folderskin.desktop",
    "~/Library/Caches/app.folderskin.desktop",
    "~/Library/Caches/folderskin-localgen",
    "~/Library/Logs/app.folderskin.desktop",
    "~/Library/Preferences/app.folderskin.desktop.plist",
    "~/Library/Saved Application State/app.folderskin.desktop.savedState",
    "~/Library/WebKit/app.folderskin.desktop",
  ]
end
