#!/usr/bin/env python3
import os
import re
import shutil

class RebrandingTool:
    def __init__(self, root_dir='.'):
        self.root_dir = root_dir

    def resolve_path(self, path):
        return os.path.join(self.root_dir, path)

    def replace_in_file(self, file_path, search_pattern, replacement, flags=re.DOTALL, skip_hint=None):
        path = self.resolve_path(file_path)
        if not os.path.exists(path):
            print(f"Warning: File {file_path} not found.")
            return

        with open(path, 'r') as f:
            content = f.read()

        # Idempotency check: if hint (or first non-empty line of replacement) is in file, skip
        hint = skip_hint if skip_hint else (replacement.split('\n')[0].strip() if replacement.strip() else None)
        if hint and hint in content:
            print(f"Skipping {file_path} - replacement (hint: '{hint}') already present.")
            return

        new_content = re.sub(search_pattern, replacement, content, flags=flags)
        if new_content != content:
            with open(path, 'w') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"No changes for {file_path} (pattern not found)")

    def replace_global(self, search, replace, excludes=None):
        if excludes is None:
            excludes = {'.git', '.next', 'node_modules', 'out', '.vscode', 'scripts'}
        
        print(f"Global replacement: '{search}' -> '{replace}'")
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in excludes]
            for file in files:
                if file.endswith(('.js', '.jsx', '.ts', '.tsx', '.css', '.md', '.mdx', '.json')):
                    file_path = os.path.relpath(os.path.join(root, file), self.root_dir)
                    self._simple_replace(file_path, search, replace)

    def _simple_replace(self, file_path, search, replace):
        path = self.resolve_path(file_path)
        with open(path, 'r') as f:
            content = f.read()
        new_content = content.replace(search, replace)
        if new_content != content:
            with open(path, 'w') as f:
                f.write(new_content)
            print(f"Updated {file_path}")

    def write_file(self, file_path, content):
        path = self.resolve_path(file_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        print(f"Created/Updated {file_path}")

    def delete_path(self, relative_path):
        path = self.resolve_path(relative_path)
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            print(f"Deleted {relative_path}")

    def delete_line(self, file_path, pattern):
        path = self.resolve_path(file_path)
        if not os.path.exists(path): return
        with open(path, 'r') as f:
            lines = f.readlines()
        
        new_lines = [l for l in lines if not re.search(pattern, l)]
        if len(new_lines) != len(lines):
            with open(path, 'w') as f:
                f.writelines(new_lines)
            print(f"Updated {file_path} (deleted lines matching '{pattern}')")

    def delete_block(self, file_path, start_pattern, end_pattern):
        path = self.resolve_path(file_path)
        if not os.path.exists(path): return
        with open(path, 'r') as f:
            content = f.read()
        
        pattern = re.escape(start_pattern) + r".*?" + re.escape(end_pattern)
        new_content = re.sub(pattern, "", content, flags=re.DOTALL)
        if new_content != content:
            with open(path, 'w') as f:
                f.write(new_content)
            print(f"Updated {file_path} (deleted block)")

    def comment_block(self, file_path, start_pattern, end_pattern):
        path = self.resolve_path(file_path)
        if not os.path.exists(path): return
        with open(path, 'r') as f:
            content = f.read()
        
        if f'{{/* {start_pattern}' in content:
            print(f"Skipping comment block in {file_path} - already commented.")
            return

        def replacer(match):
            return f"{{/* {match.group(0)} */}}"

        pattern = re.escape(start_pattern) + r".*?" + re.escape(end_pattern)
        new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
        if new_content != content:
            with open(path, 'w') as f:
                f.write(new_content)
            print(f"Updated {file_path} (commented block)")

def run_rebrand():
    tool = RebrandingTool()

    print("--- Phase 1: Global Replacements ---")
    tool.replace_global("emerald", "red")

    print("\n--- Phase 2: File Deletion ---")
    to_delete = [
        "src/app/attachments", "src/app/authentication", "src/app/contacts", 
        "src/app/conversations", "src/app/errors", "src/app/groups", 
        "src/app/messages", "src/app/pagination", "src/app/quickstart", 
        "src/app/sdks", "src/app/webhooks",
        "src/components/Libraries.jsx", "src/components/Guides.jsx", 
        "src/components/Resources.jsx", "src/components/Feedback.jsx",
        "LICENSE.md", "CHANGELOG.md"
    ]
    for p in to_delete:
        tool.delete_path(p)

    print("\n--- Phase 3: Core Branding Files ---")
    tool.write_file('src/app/page.mdx', """
export const metadata = {
  title: 'Your Gateway to Tech Excellence',
  description:
    'We offers a wealth of information, news, and insights into the ever-evolving world of technology. Whether you are a tech enthusiast, professional, or simply curious about the latest trends, TechnoBureau provides you with a one-stop hub to stay up-to-date and explore the fascinating realm of innovation.',
}

export const sections = []

## Stay Informed, Stay Ahead

Our commitment is to deliver comprehensive and engaging content that spans various areas of interest, including the latest devops tools, emerging technologies, software and apps, internet trends, cybersecurity, artificial intelligence, and much more. With a team of experienced writers and tech experts, we curate in-depth articles, insightful reviews, and thought-provoking analysis to ensure you have access to reliable and relevant information.

## Mastering Kubernetes

Unlock the full potential of container orchestration with our in-depth coverage of Kubernetes. Dive into the intricacies of Kubernetes architecture, deployment strategies, scalability, monitoring, and management techniques. TechnoBureau equips you with the knowledge and skills to confidently design, deploy, and manage scalable and resilient applications on Kubernetes, propelling your DevOps career to new heights.

## Career Advancement

TechnoBureau is dedicated to supporting your career advancement in the Linux and DevOps domains. Our comprehensive guides, career-focused articles, and expert advice offer practical insights and strategies to help you achieve your professional goals. Whether you're aiming to land your dream job, enhance your technical skills, or transition into a DevOps role, TechnoBureau provides the guidance and resources you need to succeed.
""")

    tool.write_file('src/components/Logo.jsx', """export function Logo(props) {
  return (
    <svg viewBox="0 0 129 24" aria-hidden="true" {...props}>
      <g>
        <path
          className="fill-red-400"
          d="M16 8a5 5 0 0 0-5-5H5a5 5 0 0 0-5 5v13.927a1 1 0 0 0 1.623.782l3.684-2.93a4 4 0 0 1 2.49-.87H11a5 5 0 0 0 5-5V8Z"
        />
        <text x="25" y="15" dominantBaseline="middle" className="fill-red-400">TechnoBureau</text>
      </g>
    </svg>
  );
}
""")

    tool.write_file('src/hooks/useSidebarStore.js', """'use client'
import { create } from 'zustand'

export const useSidebarStore = create()((set) => ({
  isOpen: false,
  open: () => set({ isOpen: true }),
  close: () => set({ isOpen: false }),
  toggle: () => set((state) => ({ isOpen: !state.isOpen })),
}))
""")

    print("\n--- Phase 4: Structural Adjustments (Legacy & Custom) ---")
    
    # HeroPattern Colors
    tool.replace_in_file("src/components/HeroPattern.jsx", "#36b49f", "#757272")
    tool.replace_in_file("src/components/HeroPattern.jsx", "#DBFF75", "#4e5244")

    # layout.jsx - Title and Sticky Footer
    tool.replace_in_file("src/app/layout.jsx", "Protocol API Reference", "Your Gateway to Tech Excellence")
    tool.replace_in_file("src/app/layout.jsx", r"import { Layout } from '@/components/Layout'", "import { Layout } from '@/components/Layout'\nimport { HeroPattern } from '@/components/HeroPattern'")
    tool.replace_in_file("src/app/layout.jsx", r'<div className="w-full">', """<div className="flex min-h-full w-full flex-col">
            <HeroPattern />""")

    # mdx.jsx - Feedback removal
    tool.delete_line("src/components/mdx.jsx", r"import { Feedback } from '@/components/Feedback'")
    tool.delete_line("src/components/mdx.jsx", r"<Feedback />")

    # Header.jsx - Robust Structural Swap
    header_path = 'src/components/Header.jsx'
    tool.delete_line(header_path, r"import { Button } from '@/components/Button'")
    tool.delete_block(header_path, '<div className="hidden min-[416px]:contents">', '</div>')
    tool.comment_block(header_path, '<nav className="hidden md:block">', '</nav>')
    
    tool.replace_in_file(header_path,
        r"import \{\s+MobileNavigation,.*?\} from '@\/components\/MobileNavigation'",
        """import {
  MobileNavigation,
  useIsInsideMobileNavigation,
  useMobileNavigationStore,
} from '@/components/MobileNavigation'""", skip_hint="import { MobileNavigation, useIsInsideMobileNavigation")
    
    tool.replace_in_file(header_path,
        r"import \{ ThemeToggle \} from '@\/components\/ThemeToggle'",
        "import { ThemeToggle } from '@/components/ThemeToggle'",
        skip_hint="import { ThemeToggle }")

    tool.replace_in_file(header_path,
        r"let \{ isOpen: mobileNavIsOpen,.*?\} = useMobileNavigationStore\(\)",
        "let { isOpen: mobileNavIsOpen } = useMobileNavigationStore()",
        skip_hint="let { isOpen: mobileNavIsOpen } = useMobileNavigationStore()")

    tool.delete_line(header_path, r"let \{ isOpen: sidebarIsOpen,.*?\} = useSidebarStore\(\)")
    tool.delete_line(header_path, r"let ToggleIcon = .*Icon")

    # Frozen Header ClassNames
    tool.replace_in_file(header_path,
        r"className=\{clsx\(\s+className,\s+'fixed inset-x-0 top-0 z-50.*?px-8',",
        "className={clsx(\n        className,\n        'fixed inset-x-0 top-0 z-50 flex h-14 items-center justify-between gap-12 px-4 transition-all duration-300 sm:px-6 lg:px-8',",
        skip_hint="transition-all duration-300")
    
    tool.replace_in_file(header_path,
        r"!isInsideMobileNavigation &&.*?isInsideMobileNavigation",
        "!isInsideMobileNavigation && 'backdrop-blur-xs dark:backdrop-blur-sm',\n        isInsideMobileNavigation",
        skip_hint="backdrop-blur-xs dark:backdrop-blur-sm")

    # Logo/Toggle Swap
    tool.replace_in_file(header_path,
        r'(<Search />\s+)?<div className="flex items-center gap-5 lg:hidden">.*?<Logo.*?/>.*?</CloseButton>\s+</div>(\s+<Search />)?',
        """<div className="flex flex-auto items-center gap-5">
        <Link href="/" aria-label="Home">
          <Logo className="h-6" />
        </Link>
        <MobileNavigation />
        <Search />
      </div>""", skip_hint="<div className=\"flex flex-auto items-center gap-5\">")

    # MobileNavigation.jsx - Comprehensive fix
    mob_nav_path = 'src/components/MobileNavigation.jsx'
    tool.replace_in_file(mob_nav_path,
        r"function MenuIcon\(props\) \{", "export function MenuIcon(props) {", skip_hint="export function MenuIcon")
    tool.replace_in_file(mob_nav_path,
        r"function XIcon\(props\) \{", "export function XIcon(props) {", skip_hint="export function XIcon")
    tool.replace_in_file(mob_nav_path,
        r"import \{ Navigation \} from '@\/components\/Navigation'",
        "import { Navigation } from '@/components/Navigation'\nimport { useSidebarStore } from '@/hooks/useSidebarStore'",
        skip_hint="import { useSidebarStore } from '@/hooks/useSidebarStore'")
    
    tool.replace_in_file(mob_nav_path,
        r"let \{ isOpen, toggle, close \} = useMobileNavigationStore\(\)",
        """let { isOpen: mobileNavIsOpen, toggle: toggleMobileNav, close: closeMobileNav } = useMobileNavigationStore()
  let { isOpen: sidebarIsOpen, toggle: toggleSidebar } = useSidebarStore()

  // The toggle button icon reflects BOTH states
  let isAnyOpen = mobileNavIsOpen || sidebarIsOpen
  let ToggleIcon = isAnyOpen ? XIcon : MenuIcon""", skip_hint="// The toggle button icon reflects BOTH states")

    tool.replace_in_file(mob_nav_path,
        r"isOpen=\{isOpen\} close=\{close\}",
        "isOpen={mobileNavIsOpen} close={closeMobileNav}",
        skip_hint="isOpen={mobileNavIsOpen} close={closeMobileNav}")

    tool.replace_in_file(mob_nav_path,
        r"onClick=\{toggle\}",
        """onClick={() => {
          if (typeof window !== 'undefined' && window.innerWidth >= 1024) {
            toggleSidebar()
          } else {
            toggleMobileNav()
          }
        }}""", skip_hint="if (typeof window !== 'undefined' && window.innerWidth >= 1024)")

    # Layout.jsx - Structural swap
    layout_path = 'src/components/Layout.jsx'
    tool.replace_in_file(layout_path,
        r"import \{ motion \} from 'framer-motion'",
        "import clsx from 'clsx'\nimport { motion } from 'framer-motion'",
        skip_hint="import clsx from 'clsx'")

    tool.replace_in_file(layout_path,
        r"import \{ usePathname \} from 'next\/navigation'",
        "import { usePathname } from 'next/navigation'\nimport { useSidebarStore } from '@/hooks/useSidebarStore'",
        skip_hint="import { useSidebarStore } from '@/hooks/useSidebarStore'")
    
    tool.replace_in_file(layout_path,
        r"let pathname = usePathname\(\)",
        "let pathname = usePathname()\n  let { isOpen } = useSidebarStore()",
        skip_hint="let { isOpen } = useSidebarStore()")

    tool.replace_in_file(layout_path,
        r'<div className="h-full lg:ml-72 xl:ml-80">.*?</div>\s+</SectionProvider>',
        """<div
        className="group relative flex flex-auto flex-col"
        data-sidebar-collapsed={!isOpen ? '' : undefined}
      >
        <Header />

        <aside className="fixed bottom-0 left-0 top-14 z-40 w-72 -translate-x-full overflow-y-auto border-r border-zinc-900/10 bg-white px-6 pt-6 pb-8 transition-transform duration-300 ease-in-out lg:not-group-data-sidebar-collapsed:translate-x-0 max-lg:hidden xl:w-80 lg:dark:border-white/10 dark:bg-zinc-900">
          <Navigation />
        </aside>

        <div
          className={clsx(
            'flex flex-auto flex-col transition-all duration-300 ease-in-out',
            'lg:pl-0 lg:not-group-data-sidebar-collapsed:pl-72 xl:not-group-data-sidebar-collapsed:pl-80',
          )}
        >
          <div className="relative flex flex-auto flex-col px-4 pt-14 sm:px-6 lg:px-8">
            <main className="flex-auto">{children}</main>
            <Footer />
          </div>
        </div>
      </div>
    </SectionProvider>""", skip_hint="data-sidebar-collapsed")

    # Navigation.jsx logic
    nav_path = 'src/components/Navigation.jsx'
    tool.replace_in_file(nav_path, r"\{ title: 'Quickstart', href: '/quickstart' \},", "{ title: 'DevOps', href: '/devops' },")
    tool.replace_in_file(nav_path, r"\{ title: 'SDKs', href: '/sdks' \},", "{ title: 'Kubernetes', href: '/kubernetes' },")
    tool.replace_in_file(nav_path, r"\{ title: 'Authentication', href: '/authentication' \},", "{ title: 'Linux', href: '/linux' },\n      { title: 'Career', href: '/career' },")
    
    tool.replace_in_file(nav_path,
        r'let activePageIndex = group.links.findIndex.*?let top = offset .*? itemHeight',
        """  // Use the same absolute index calculation as VisibleSectionHighlight
  let absoluteIndex = 0
  let targetIndex = 0

  for (let i = 0; i < group.links.length; i++) {
    const link = group.links[i]
    if (link.href === pathname) {
      targetIndex = absoluteIndex
    }
    absoluteIndex++

    if (link.links) {
      for (let j = 0; j < link.links.length; j++) {
        if (link.links[j].href === pathname) {
          targetIndex = absoluteIndex
        }
        absoluteIndex++
      }
    }
  }
  let top = offset + targetIndex * itemHeight""", skip_hint="let targetIndex = 0")

    tool.replace_in_file(nav_path,
        r'function NavLink\({.*?}\) \{.*?return \(.*?<Component.*?>(.*?)</Component>.*?\(.*?\)',
        """function NavLink({
  href,
  children,
  tag,
  active = false,
  isAnchorLink = false,
}) {
  let isInsideMobileNavigation = useIsInsideMobileNavigation()
  // Safety check: even if the context says we are inside mobile navigation, 
  // if we are on a large screen, assume we are in the desktop sidebar.
  let isMobile = isInsideMobileNavigation && typeof window !== 'undefined' && window.innerWidth < 1024
  let Component = isMobile ? CloseButton : Link

  return (
    <Component
      href={href}
      {...(isMobile ? { as: Link } : {})}
      aria-current={active ? 'page' : undefined}
      className={clsx(
        'flex justify-between gap-2 py-1 pr-3 text-sm transition',
        isAnchorLink ? 'pl-7' : 'pl-4',
        active
          ? 'text-zinc-900 dark:text-white'
          : 'text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white',
      )}
    >
      <span className="truncate">{children}</span>
      {tag && (
        <Tag variant="small" color="zinc">
          {tag}
        </Tag>
      )}
    </Component>
  )
}""", skip_hint="window.innerWidth < 1024")

    # Width expansions
    tool.replace_in_file('src/components/Search.jsx', r'lg:max-w-md lg:flex-auto', 'lg:max-w-2xl lg:flex-auto')
    tool.replace_in_file('src/components/Footer.jsx',
        r'footer className="mx-auto w-full max-w-2xl space-y-10 pb-2 lg:max-w-5xl"',
        'footer className="mx-auto w-full max-w-2xl space-y-10 pb-2 lg:max-w-5xl group-data-sidebar-collapsed:lg:max-w-7xl"')
    tool.replace_in_file('typography.js', r"fontSize: theme\('fontSize.2xs'\),", r"fontSize: theme('fontSize.2xs')[0],")

    # Button.jsx - Fix plain prop to prevent React warning
    button_path = 'src/components/Button.jsx'
    tool.replace_in_file(button_path,
        r'export function Button\(\{\s+variant = \'primary\',\s+className,\s+children,\s+arrow,\s+\.\.\.props\s+\}\)',
        """export function Button({
  variant = 'primary',
  className,
  children,
  arrow,
  plain, // Destructure plain to prevent it from leaking to props
  ...props
})""",
        skip_hint="plain, // Destructure plain to prevent it from leaking to props")

    print("\nRebranding complete!")

if __name__ == "__main__":
    run_rebrand()
