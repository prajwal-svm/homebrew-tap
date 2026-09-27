class FolderskinCli < Formula
  desc "Command-line tool for custom folder icons, skin packs and local AI painting"
  homepage "https://folderskin.app/"
  license "GPL-3.0-only"

  livecheck do
    url :stable
    regex(/^cli-v?(\d+(?:\.\d+)+)$/i)
    strategy :github_releases
  end

  on_macos do
    on_arm do
      url "https://github.com/prajwal-svm/folderskin/releases/download/cli-v0.1.0/folderskin-cli-0.1.0-macos-universal.tar.gz"
      sha256 "7351b73f2f89ee591c285bc8ebad6e81d8609f4e6d79af06fc00c0977b476983"
    end
    on_intel do
      url "https://github.com/prajwal-svm/folderskin/releases/download/cli-v0.1.0/folderskin-cli-0.1.0-macos-universal.tar.gz"
      sha256 "7351b73f2f89ee591c285bc8ebad6e81d8609f4e6d79af06fc00c0977b476983"
    end
  end

  on_linux do
    on_intel do
      url "https://github.com/prajwal-svm/folderskin/releases/download/cli-v0.1.0/folderskin-cli-0.1.0-linux-x86_64.tar.gz"
      sha256 "1b877bca52889bdae8de16c16e10b4d1fbefee911256d1172624e0942e955f10"
    end
    on_arm do
      url "https://github.com/prajwal-svm/folderskin/releases/download/cli-v0.1.0/folderskin-cli-0.1.0-linux-aarch64.tar.gz"
      sha256 "a72d59edf320971d2a48c2b01b5b3d3db333a88afd244b1b07bef45e2fcaebbe"
    end
  end

  def install
    bin.install "folderskin"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/folderskin --version")
  end
end
