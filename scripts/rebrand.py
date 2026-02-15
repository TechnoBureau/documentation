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

    print("\n--- Phase 3: Applying Customizations (Snapshot Restoration) ---")
    
    # 1. Page MDX
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
    
    # 2. Logo
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
    
    # 3. Sidebar Store
    tool.write_file('src/hooks/useSidebarStore.js', """'use client'
import { create } from 'zustand'

export const useSidebarStore = create()((set) => ({
  isOpen: false,
  open: () => set({ isOpen: true }),
  close: () => set({ isOpen: false }),
  toggle: () => set((state) => ({ isOpen: !state.isOpen })),
}))
""")

    # 4. Navigation
    # Replace the navigation array
    tool.replace_in_file(
        'src/components/Navigation.jsx',
        r'export const navigation = \[[\s\S]*?\]',
        """export const navigation = [
  {
    title: 'Guides',
    links: [
      { title: 'Introduction', href: '/' },
      {
        title: 'DevOps', href: '/devops',
        links: [
          { title: 'General', href: '/devops/general' },
          { title: 'CI/CD', href: '/devops/ci-cd' },
          { title: 'Terraform', href: '/devops/terraform' },
          // { title: 'Ansible', href: '/devops/ansible' },
        ]
      },
      {
        title: 'Kubernetes', href: '/kubernetes',
        links: [
          { title: 'General', href: '/kubernetes/general' },
          { title: 'Deployment', href: '/kubernetes/deployment' },
          // { title: 'Services', href: '/kubernetes/services' },
        ]
      },
      {
        title: 'Linux',
        href: '/linux',
        links: [
          { title: 'General', href: '/linux/general' },
          { title: 'System Administration', href: '/linux/administration' },
          { title: 'MySQL', href: '/linux/mysql' },
        ]
      },
      {
        title: 'Career',
        href: '/career',
        links: [
          { title: 'General', href: '/career/general' },
        ]
      },
    ],
  },
]"""
    )

    # Ensure navigation container is excluded from snippets
    tool.replace_in_file(
        'src/components/Navigation.jsx',
        r'<nav \{\.\.\.props\}>',
        """<nav data-nosnippet {...props}>"""
    )

    # 5. Mobile Navigation
    # Replace the MobileNavigation component and store
    tool.replace_in_file(
        'src/components/MobileNavigation.jsx',
        r'export const useMobileNavigationStore = create[\s\S]*?\)\)',
        """export const useMobileNavigationStore = create()((set) => ({
  isOpen: false,
  open: () => set({ isOpen: true }),
  close: () => set({ isOpen: false }),
  toggle: () => set((state) => ({ isOpen: !state.isOpen })),
}))"""
    )
    
    # Replace MobileNavigation main component
    tool.replace_in_file(
        'src/components/MobileNavigation.jsx',
        r'export function MobileNavigation\(\) \{[\s\S]*?\}',
        """export function MobileNavigation() {
  let isInsideMobileNavigation = useIsInsideMobileNavigation()
  let { isOpen: mobileNavIsOpen, toggle: toggleMobileNav, close: closeMobileNav } = useMobileNavigationStore()
  let { isOpen: sidebarIsOpen, toggle: toggleSidebar } = useSidebarStore()

  // The toggle button icon reflects BOTH states
  let isAnyOpen = mobileNavIsOpen || sidebarIsOpen
  let ToggleIcon = isAnyOpen ? XIcon : MenuIcon

  return (
    <IsInsideMobileNavigationContext.Provider value={true}>
      <button
        type="button"
        className="relative flex size-6 items-center justify-center rounded-md transition hover:bg-zinc-900/5 dark:hover:bg-white/5"
        aria-label="Toggle navigation"
        onClick={() => {
          if (window.innerWidth >= 1024) {
            toggleSidebar()
          } else {
            toggleMobileNav()
          }
        }}
      >
        <span className="absolute size-12 pointer-fine:hidden" />
        <ToggleIcon className="w-2.5 stroke-zinc-900 dark:stroke-white" />
      </button>
      {!isInsideMobileNavigation && (
        <Suspense fallback={null}>
          <MobileNavigationDialog isOpen={mobileNavIsOpen} close={closeMobileNav} />
        </Suspense>
      )}
    </IsInsideMobileNavigationContext.Provider>
  )
}"""
    )
    
    # Ensure useSidebarStore is imported
    tool.replace_in_file(
        'src/components/MobileNavigation.jsx',
        r'import \{ Navigation \} from \'@/components/Navigation\'',
        """import { Navigation } from '@/components/Navigation'
import { useSidebarStore } from '@/hooks/useSidebarStore'"""
    )

    # Ensure mobile navigation dialog/drawer text is excluded from snippets
    tool.replace_in_file(
        'src/components/MobileNavigation.jsx',
        r'<Dialog\s+transition\s+open=\{isOpen\}\s+onClose=\{close\}',
        """<Dialog
      transition
      open={isOpen}
      onClose={close}
      data-nosnippet"""
    )
    tool.replace_in_file(
        'src/components/MobileNavigation.jsx',
        r'<motion\.div\s+layoutScroll',
        """<motion.div
            layoutScroll
            data-nosnippet"""
    )


    # 6. Header
    # Replace the Header component
    tool.replace_in_file(
        'src/components/Header.jsx',
        r'export const Header = forwardRef\([\s\S]*?\)\s*',
        """export const Header = forwardRef(function Header({ className, ...props }, ref) {
  let { isOpen: mobileNavIsOpen } = useMobileNavigationStore()
  let isInsideMobileNavigation = useIsInsideMobileNavigation()

  let { scrollY } = useScroll()
  let bgOpacityLight = useTransform(scrollY, [0, 72], ['50%', '90%'])
  let bgOpacityDark = useTransform(scrollY, [0, 72], ['20%', '80%'])


  return (
    <motion.div
      {...props}
      ref={ref}
      data-nosnippet
      className={clsx(
        className,
        'fixed inset-x-0 top-0 z-50 flex h-14 items-center justify-between gap-12 px-4 transition-all duration-300 sm:px-6 lg:px-8',
        !isInsideMobileNavigation && 'backdrop-blur-xs dark:backdrop-blur-sm',
        isInsideMobileNavigation
          ? 'bg-white dark:bg-zinc-900'
          : 'bg-white/(--bg-opacity-light) dark:bg-zinc-900/(--bg-opacity-dark)',
      )}
      style={{
        '--bg-opacity-light': bgOpacityLight,
        '--bg-opacity-dark': bgOpacityDark,
      }}
    >
      <div
        className={clsx(
          'absolute inset-x-0 top-full h-px transition',
          (isInsideMobileNavigation || !mobileNavIsOpen) &&
          'bg-zinc-900/7.5 dark:bg-white/7.5',
        )}
      />
      <div className="flex flex-auto items-center gap-5">
        <Link href="/" aria-label="Home">
          <Logo className="h-6" />
        </Link>
        <MobileNavigation />
        <Search />
      </div>
      <div className="flex items-center gap-5">
        {/* <nav className="hidden md:block">
          <ul role="list" className="flex items-center gap-8">
            <TopLevelNavItem href="/devops">DevOps</TopLevelNavItem>
            <TopLevelNavItem href="/kubernetes">Kubernetes</TopLevelNavItem>
            <TopLevelNavItem href="/linux">Linux</TopLevelNavItem>
          </ul>
        </nav> */}
        <div className="hidden md:block md:h-5 md:w-px md:bg-zinc-900/10 md:dark:bg-white/15" />
        <div className="flex gap-4">
          <MobileSearch />
          <ThemeToggle />
        </div>
      </div>
    </motion.div>
  )
})
"""
    )
    
    # Ensure imports for Header logic
    tool.replace_in_file(
        'src/components/Header.jsx',
        r'import \{ MobileNavigation, useIsInsideMobileNavigation \} from \'@/components/MobileNavigation\'',
        """import {
  MobileNavigation,
  useIsInsideMobileNavigation,
  useMobileNavigationStore,
} from '@/components/MobileNavigation'"""
    )
    
    tool.replace_in_file(
        'src/components/Header.jsx',
        r'import \{ ThemeToggle \} from \'@/components/ThemeToggle\'',
        """import { ThemeToggle } from '@/components/ThemeToggle'
import { useSidebarStore } from '@/hooks/useSidebarStore'"""
    )


    # 7. App Layout
    # Replace metadata and root layout content
    tool.replace_in_file(
        'src/app/layout.jsx',
        r'export const metadata = \{[\s\S]*?\}',
        """export const metadata = {
  metadataBase: new URL('https://technobureau.com'),
  title: {
    template: '%s - Your Gateway to Tech Excellence',
    default: 'Your Gateway to Tech Excellence',
  },
  siteName: 'TechnoBureau',
  generator: 'TechnoBureau',
  locale: 'en_US',
  type: 'article',
  description: 'We offers a wealth of information, news, and insights into the ever-evolving world of technology. Whether you are a tech enthusiast, professional, or simply curious about the latest trends, TechnoBureau provides you with a one-stop hub to stay up-to-date and explore the fascinating realm of innovation',
  keywords: "documentation,technical guides,development,programming",
  authors: [{ name: 'Ganapathi Chidambaram', url: 'https://github.com/GanapathiChidambaram' }],
  referrer: 'origin-when-cross-origin',
  creator: 'Ganapathi Chidambaram',
  publisher: 'TechnoBureau',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    siteName: 'TechnoBureau',
    locale: 'en_US',
    type: 'article',
    authors: ['Ganapathi Chidambaram'],
  },
  twitter: {
    card: 'summary_large_image',
    creator: '@ganapathirj',
  },
  robots: {
    index: true,
    follow: true,
    nocache: false,
    googleBot: {
      index: true,
      follow: true,
      noimageindex: false,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
      },
  },
}"""
    )
    
    # RootLayout Replacement - Inject HeroPattern and custom Layout attributes
    # We aim to replace the return (...) block of RootLayout
    tool.replace_in_file(
        'src/app/layout.jsx',
        r'return \(\s*<html[\s\S]*?</html>\s*\)',
        """return (
    <html lang="en" className="h-full" suppressHydrationWarning>
      <body className="flex min-h-full bg-white antialiased dark:bg-zinc-900">
        <Providers>
          <div className="flex min-h-full w-full flex-col">
            <HeroPattern />
            <Layout allSections={allSections}>{children}</Layout>
          </div>
        </Providers>
      </body>
    </html>
  )"""
    )
    
    # Ensure HeroPattern is imported
    tool.replace_in_file(
        'src/app/layout.jsx',
        r'import { Layout } from \'@/components/Layout\'',
        """import { Layout } from '@/components/Layout'
import { HeroPattern } from '@/components/HeroPattern'"""
    )


    # 8. Components Layout
    # Replace the Layout component
    tool.replace_in_file(
        'src/components/Layout.jsx',
        r'export function Layout\(\{[\s\S]*?\}',
        """export function Layout({ children, allSections }) {
  let pathname = usePathname()
  let { isOpen } = useSidebarStore()

  return (
    <SectionProvider sections={allSections[pathname] ?? []}>
      <div
        className="group relative flex flex-auto flex-col"
        data-sidebar-collapsed={!isOpen ? '' : undefined}
      >
        <Header />

        <aside data-nosnippet className="fixed bottom-0 left-0 top-14 z-40 w-72 -translate-x-full overflow-y-auto border-r border-zinc-900/10 bg-white px-6 pt-6 pb-8 transition-transform duration-300 ease-in-out lg:not-group-data-sidebar-collapsed:translate-x-0 max-lg:hidden xl:w-80 lg:dark:border-white/10 dark:bg-zinc-900">
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
    </SectionProvider>
  )
}"""
    )
    
    # Ensure imports for Layout
    tool.replace_in_file(
        'src/components/Layout.jsx',
        r'import \{ Navigation \} from \'@/components/Navigation\'',
        """import { Navigation } from '@/components/Navigation'
import { useSidebarStore } from '@/hooks/useSidebarStore'"""
    )


    # 9. Button
    # Replace Button component and styles
    tool.replace_in_file(
        'src/components/Button.jsx',
        r'const variantStyles = \{[\s\S]*?\}',
        """const variantStyles = {
  primary:
    'rounded-full bg-zinc-900 py-1 px-3 text-white hover:bg-zinc-700 dark:bg-red-400/10 dark:text-red-400 dark:ring-1 dark:ring-inset dark:ring-red-400/20 dark:hover:bg-red-400/10 dark:hover:text-red-300 dark:hover:ring-red-300',
  secondary:
    'rounded-full bg-zinc-100 py-1 px-3 text-zinc-900 hover:bg-zinc-200 dark:bg-zinc-800/40 dark:text-zinc-400 dark:ring-1 dark:ring-inset dark:ring-zinc-800 dark:hover:bg-zinc-800 dark:hover:text-zinc-300',
  filled:
    'rounded-full bg-zinc-900 py-1 px-3 text-white hover:bg-zinc-700 dark:bg-red-500 dark:text-white dark:hover:bg-red-400',
  outline:
    'rounded-full py-1 px-3 text-zinc-700 ring-1 ring-inset ring-zinc-900/10 hover:bg-zinc-900/2.5 hover:text-zinc-900 dark:text-zinc-400 dark:ring-white/10 dark:hover:bg-white/5 dark:hover:text-white',
  text: 'text-red-500 hover:text-red-600 dark:text-red-400 dark:hover:text-red-500',
}"""
    )
    
    tool.replace_in_file(
        'src/components/Button.jsx',
        r'export function Button\(\{[\s\S]*?\}',
        """export function Button({
  variant = 'primary',
  className,
  children,
  arrow,
  plain, // Destructure plain to prevent it from leaking to props
  ...props
}) {
  className = clsx(
    variant !== 'plain' && 'inline-flex gap-0.5 justify-center overflow-hidden text-sm font-medium transition',
    variantStyles[variant],
    className,
  )

  let arrowIcon = (
    <ArrowIcon
      className={clsx(
        'mt-0.5 h-5 w-5',
        variant === 'text' && 'relative top-px',
        arrow === 'left' && '-ml-1 rotate-180',
        arrow === 'right' && '-mr-1',
      )}
    />
  )

  let inner = (
    <>
      {arrow === 'left' && arrowIcon}
      {children}
      {arrow === 'right' && arrowIcon}
    </>
  )

  if (props.href === undefined) {
    return (
      <button className={className} {...props}>
        {inner}
      </button>
    )
  }

  return (
    <Link className={className} {...props}>
      {inner}
    </Link>
  )
}"""
    )


    # 10. Search
    # Replace Search components
    tool.replace_in_file(
        'src/components/Search.jsx',
        r'function SearchDialog\(\{[\s\S]*?\n\}\)',
        """function SearchDialog({ open, setOpen, className }) {
  let formRef = useRef(null)
  let panelRef = useRef(null)
  let inputRef = useRef(null)
  let { close } = useMobileNavigationStore()

  let autocomplete = createAutocomplete({
    onStateChange({ state }) {
      if (state.status === 'stalled') {
        if (state.collections.length > 0) {
          setAutocompleteState(state)
        }
      } else {
        setAutocompleteState(state)
      }
    },
    onSubmit({ state }) {
      if (state.collections.length > 0 && state.collections[0].items.length > 0) {
        let { url } = state.collections[0].items[0]
        close()
        window.location.href = url
      }
    },
    navigator: {
      navigate({ itemUrl }) {
        setOpen(false)
        close()
        window.location.href = itemUrl
      },
      navigateNewTab({ itemUrl }) {
        let windowReference = window.open(itemUrl, '_blank', 'noopener')
        if (windowReference) {
          windowReference.focus()
        }
      },
      navigateNewWindow({ itemUrl }) {
        window.open(itemUrl, '_blank', 'noopener')
      },
    },
    getSources({ query }) {
      return import('@/mdx/search.mjs').then(({ search }) => {
        return [
          {
            sourceId: 'documentation',
            getItems() {
              return search(query, { limit: 5 })
            },
            getItemUrl({ item }) {
              return item.url
            },
            onSelect({ itemUrl }) {
              setOpen(false)
              close()
              window.location.href = itemUrl
            },
          },
        ]
      })
    },
  })

  let [autocompleteState, setAutocompleteState] = useState(
    autocomplete.getState(),
  )

  useEffect(() => {
    if (!open) {
      return
    }

    function onKeyDown(event) {
      if (event.key === 'k' && (event.metaKey || event.ctrlKey)) {
        event.preventDefault()
        setOpen(false)
      }
    }

    window.addEventListener('keydown', onKeyDown)

    return () => {
      window.removeEventListener('keydown', onKeyDown)
    }
  }, [open, setOpen])

  return (
    <Dialog
      data-nosnippet
      open={open}
      onClose={() => {
        setOpen(false)
        autocomplete.setQuery('')
      }}
      className={clsx('fixed inset-0 z-50', className)}
    >
      <DialogPanel className="fixed inset-0 bg-zinc-400/25 backdrop-blur-sm dark:bg-black/40" />

      <div className="fixed inset-0 overflow-y-auto px-4 py-4 sm:px-6 sm:py-20 md:py-32 lg:px-8 lg:py-[15vh]">
        <DialogPanel className="mx-auto transform-gpu overflow-hidden rounded-xl bg-white shadow-xl ring-1 ring-zinc-900/5 sm:max-w-xl dark:bg-zinc-900 dark:ring-zinc-800">
          <div {...autocomplete.getRootProps({})}>
            <form
              ref={formRef}
              {...autocomplete.getFormProps({
                inputElement: inputRef.current,
              })}
            >
              <div data-nosnippet className="flex h-12 items-center gap-2 border-b border-zinc-900/7.5 px-4 dark:border-white/7.5">
                <SearchIcon className="h-5 w-5 fill-zinc-500 dark:fill-zinc-400" />
                <input
                  ref={inputRef}
                  className="flex-auto appearance-none bg-transparent pl-2 text-zinc-900 placeholder:text-zinc-500 focus:outline-none dark:text-white dark:placeholder:text-zinc-400"
                  {...autocomplete.getInputProps({
                    placeholder: 'Find something...',
                    autoFocus: true,
                    onKeyDown(event) {
                      if (
                        event.key === 'Escape' &&
                        inputRef.current?.value === ''
                      ) {
                        setOpen(false)
                        event.preventDefault()
                      }
                    },
                  })}
                />
              </div>
              <div
                ref={panelRef}
                className="max-h-96 overflow-y-auto px-4 py-2 border-t border-zinc-100 dark:border-zinc-800 empty:hidden"
                {...autocomplete.getPanelProps({})}
              >
                {autocompleteState.isOpen && (
                  <SearchResults
                    autocomplete={autocomplete}
                    query={autocompleteState.query}
                    collection={autocompleteState.collections[0]}
                  />
                )}
              </div>
            </form>
          </div>
        </DialogPanel>
      </div>
    </Dialog>
  )
}"""
    )

    tool.replace_in_file(
        'src/components/Search.jsx',
        r'export function Search\(\) \{[\s\S]*?\n\}',
        """export function Search() {
  let [modifierKey, setModifierKey] = useState()
  let { buttonProps, dialogProps } = useSearchProps()

  useEffect(() => {
    setModifierKey(
      /(Mac|iPhone|iPod|iPad)/i.test(navigator.platform) ? '⌘' : 'Ctrl ',
    )
  }, [])

  return (
    <div className="hidden lg:block lg:max-w-2xl lg:flex-auto" data-nosnippet>
      <button
        data-nosnippet
        type="button"
        className="hidden h-8 w-full items-center gap-2 rounded-full bg-white pr-3 pl-2 text-sm text-zinc-500 ring-1 ring-zinc-900/10 transition hover:ring-zinc-900/20 lg:flex dark:bg-white/5 dark:text-zinc-400 dark:ring-white/10 dark:ring-inset dark:hover:ring-white/20"
        {...buttonProps}
      >
        <SearchIcon className="h-5 w-5 stroke-current" />
        Find something...
        <kbd className="ml-auto text-2xs text-zinc-400 dark:text-zinc-500" data-nosnippet>
          <kbd className="font-sans">{modifierKey}</kbd>
          <kbd className="font-sans">K</kbd>
        </kbd>
      </button>
      <Suspense fallback={null}>
        <SearchDialog className="hidden lg:block" {...dialogProps} />
      </Suspense>
    </div>
  )
}"""
    )
    
    tool.replace_in_file(
        'src/components/Search.jsx',
        r'export function MobileSearch\(\) \{[\s\S]*?\n\}',
        """export function MobileSearch() {
  let { close } = useMobileNavigationStore()
  let { buttonProps, dialogProps } = useSearchProps()

  return (
    <div className="contents lg:hidden" data-nosnippet>
      <button
        data-nosnippet
        type="button"
        className="relative flex size-6 items-center justify-center rounded-md transition hover:bg-zinc-900/5 lg:hidden dark:hover:bg-white/5"
        aria-label="Find something..."
        {...buttonProps}
      >
        <span className="absolute size-12 pointer-fine:hidden" />
        <SearchIcon className="h-5 w-5 stroke-zinc-900 dark:stroke-white" />
      </button>
      <Suspense fallback={null}>
        <SearchDialog
          className="lg:hidden"
          onNavigate={close}
          {...dialogProps}
        />
      </Suspense>
    </div>
  )
}"""
    )

    # 11. Footer
    # Replace Footer components
    tool.replace_in_file(
        'src/components/Footer.jsx',
        r'function SmallPrint\(\) \{[\s\S]*?\}',
        """function SmallPrint() {
  return (
    <div className="flex flex-col items-center justify-between gap-5 border-t border-zinc-900/5 pt-2 sm:flex-row dark:border-white/5">
      <p className="text-xs text-zinc-600 dark:text-zinc-400">
        &copy; Copyright {new Date().getFullYear()}. All rights reserved.
      </p>
      <div className="flex gap-4">
        <SocialLink href="#" icon={GitHubIcon}>
          Follow us on GitHub
        </SocialLink>
      </div>
    </div>
  )
}"""
    )

    tool.replace_in_file(
        'src/components/Footer.jsx',
        r'export function Footer\(\) \{[\s\S]*?\}',
        """export function Footer() {
  return (
    <footer data-nosnippet className="mx-auto w-full max-w-2xl space-y-10 pb-2 lg:max-w-5xl group-data-sidebar-collapsed:lg:max-w-7xl">
      <PageNavigation />
      <SmallPrint />
    </footer>
  )
}"""
    )

    # 12. Article Listing and Article Grid
    tool.write_file(
        'src/components/ArticleListing.jsx',
        """import Link from 'next/link'
import { formatDate } from '@/lib/formatDate'

export function Article({ article, basePath }) {
    const articleHref = `${basePath}/${article.slug}`
    const parsedDate = new Date(`${article.date}T00:00:00`)
    const month = parsedDate.toLocaleDateString('en-US', { month: 'short' }).toUpperCase()
    const day = parsedDate.toLocaleDateString('en-US', { day: 'numeric' })
    const year = parsedDate.toLocaleDateString('en-US', { year: 'numeric' })

    return (
        <article className="group relative">
            <div className="relative overflow-hidden rounded-3xl border border-zinc-200 bg-zinc-50/70 p-6 shadow-sm ring-1 ring-zinc-900/5 dark:border-zinc-700 dark:bg-zinc-900/70 dark:ring-white/10 sm:p-8">
                <div className="relative z-10 flex flex-col gap-5 sm:flex-row sm:items-start sm:gap-6">
                    <div className="flex items-start sm:shrink-0">
                        <time
                            dateTime={article.date}
                            title={formatDate(article.date)}
                            className="inline-flex w-[4.5rem] flex-col overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm ring-1 ring-zinc-900/5 dark:border-zinc-700 dark:bg-zinc-900 dark:ring-white/10"
                        >
                            <span className="bg-red-500 px-2 py-1 text-center text-[0.62rem] font-bold tracking-[0.08em] text-white">
                                {month}
                            </span>
                            <span className="px-2 pt-2 pb-1 text-center text-2xl font-bold leading-none text-zinc-900 dark:text-zinc-100">
                                {day}
                            </span>
                            <span className="px-2 pb-2 text-center text-[0.62rem] font-semibold tracking-[0.08em] text-zinc-500 dark:text-zinc-400">
                                {year}
                            </span>
                        </time>
                    </div>

                    <div className="min-w-0 flex-1">
                        <h2 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
                            <Link
                                href={articleHref}
                                className="outline-none"
                            >
                                {article.title}
                            </Link>
                        </h2>

                        <p className="mt-4 text-base leading-8 text-zinc-600 dark:text-zinc-400">
                            {article.description}
                        </p>

                        <div className="mt-6">
                            <Link
                                href={articleHref}
                                className="inline-flex items-center gap-1.5 text-base font-semibold text-teal-600 dark:text-teal-400"
                            >
                                Read article
                                <svg
                                    viewBox="0 0 16 16"
                                    fill="none"
                                    aria-hidden="true"
                                    className="h-4 w-4 stroke-current"
                                >
                                    <path
                                        d="M6.75 5.75 9.25 8l-2.5 2.25"
                                        strokeWidth="1.5"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                    />
                                </svg>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </article>
    )
}
""")

    tool.write_file(
        'src/components/PaginatedArticles.jsx',
        """'use client'

import { useSearchParams } from 'next/navigation'
import { Suspense } from 'react'
import { ArticlesPagination } from '@/components/ArticlesPagination'
import { Article } from '@/components/ArticleListing'

function PaginatedArticlesInner({ allArticles, pageSize, basePath }) {
    const searchParams = useSearchParams()
    const currentPage = parseInt(searchParams.get('page') || '1', 10)

    const totalArticles = allArticles.length
    const articles = allArticles.slice(
        (currentPage - 1) * pageSize,
        currentPage * pageSize
    )

    return (
        <>
            <div className="flex w-full max-w-none flex-col gap-6 pb-8 sm:pb-10">
                {articles.length > 0 ? (
                    articles.map((article) => (
                        <Article key={article.slug} article={article} basePath={basePath} />
                    ))
                ) : (
                    <p className="rounded-2xl border border-zinc-200/80 bg-zinc-50/80 p-8 text-center text-zinc-600 dark:border-zinc-700 dark:bg-zinc-800/60 dark:text-zinc-400">
                        No articles found.
                    </p>
                )}
            </div>

            <ArticlesPagination
                totalArticles={totalArticles}
                pageSize={pageSize}
                currentPage={currentPage}
                basePath={basePath}
            />
        </>
    )
}

export function PaginatedArticles({ allArticles, pageSize, basePath }) {
    return (
        <Suspense
            fallback={
                <div className="rounded-2xl border border-zinc-200/80 bg-zinc-50/80 p-8 text-center text-zinc-600 dark:border-zinc-700 dark:bg-zinc-800/60 dark:text-zinc-400">
                    Loading articles...
                </div>
            }
        >
            <PaginatedArticlesInner
                allArticles={allArticles}
                pageSize={pageSize}
                basePath={basePath}
            />
        </Suspense>
    )
}
""")

    # 13. Typography
    # 13. Typography
    # Replace the typography theme logic
    tool.replace_in_file(
        'typography.js',
        r'typography: \(\{ theme \}\) => \(\{[\s\S]*?\}\)\,',
        """typography: ({ theme }) => ({
      DEFAULT: {
        css: {
          '--tw-prose-body': theme('colors.zinc.700'),
          '--tw-prose-headings': theme('colors.zinc.900'),
          '--tw-prose-links': theme('colors.red.500'),
          '--tw-prose-links-hover': theme('colors.red.600'),
          '--tw-prose-links-underline': theme('colors.red.500 / 0.3'),
          '--tw-prose-bold': theme('colors.zinc.900'),
          '--tw-prose-counters': theme('colors.zinc.500'),
          '--tw-prose-bullets': theme('colors.zinc.300'),
          '--tw-prose-hr': theme('colors.zinc.900 / 0.05'),
          '--tw-prose-quotes': theme('colors.zinc.900'),
          '--tw-prose-quote-borders': theme('colors.zinc.200'),
          '--tw-prose-captions': theme('colors.zinc.500'),
          '--tw-prose-code': theme('colors.zinc.900'),
          '--tw-prose-code-bg': theme('colors.zinc.100'),
          '--tw-prose-code-ring': theme('colors.zinc.300'),
          '--tw-prose-th-borders': theme('colors.zinc.300'),
          '--tw-prose-td-borders': theme('colors.zinc.200'),

          '--tw-prose-invert-body': theme('colors.zinc.400'),
          '--tw-prose-invert-headings': theme('colors.white'),
          '--tw-prose-invert-links': theme('colors.red.400'),
          '--tw-prose-invert-links-hover': theme('colors.red.500'),
          '--tw-prose-invert-links-underline': theme(
            'colors.red.500 / 0.3',
          ),
          '--tw-prose-invert-bold': theme('colors.white'),
          '--tw-prose-invert-counters': theme('colors.zinc.400'),
          '--tw-prose-invert-bullets': theme('colors.zinc.600'),
          '--tw-prose-invert-hr': theme('colors.white / 0.05'),
          '--tw-prose-invert-quotes': theme('colors.zinc.100'),
          '--tw-prose-invert-quote-borders': theme('colors.zinc.700'),
          '--tw-prose-invert-captions': theme('colors.zinc.400'),
          '--tw-prose-invert-code': theme('colors.white'),
          '--tw-prose-invert-code-bg': theme('colors.zinc.700 / 0.15'),
          '--tw-prose-invert-code-ring': theme('colors.white / 0.1'),
          '--tw-prose-invert-th-borders': theme('colors.zinc.600'),
          '--tw-prose-invert-td-borders': theme('colors.zinc.700'),

          // Base
          color: 'var(--tw-prose-body)',
          fontSize: theme('fontSize.sm')[0],
          lineHeight: theme('lineHeight.7'),

          // Text
          p: {
            marginTop: theme('spacing.6'),
            marginBottom: theme('spacing.6'),
          },
          '[class~="lead"]': {
            fontSize: theme('fontSize.base')[0],
            ...theme('fontSize.base')[1],
          },

          // Lists
          ol: {
            listStyleType: 'decimal',
            marginTop: theme('spacing.5'),
            marginBottom: theme('spacing.5'),
            paddingLeft: '1.625rem',
          },
          'ol[type="A"]': {
            listStyleType: 'upper-alpha',
          },
          'ol[type="a"]': {
            listStyleType: 'lower-alpha',
          },
          'ol[type="A" s]': {
            listStyleType: 'upper-alpha',
          },
          'ol[type="a" s]': {
            listStyleType: 'lower-alpha',
          },
          'ol[type="I"]': {
            listStyleType: 'upper-roman',
          },
          'ol[type="i"]': {
            listStyleType: 'lower-roman',
          },
          'ol[type="I" s]': {
            listStyleType: 'upper-roman',
          },
          'ol[type="i" s]': {
            listStyleType: 'lower-roman',
          },
          'ol[type="1"]': {
            listStyleType: 'decimal',
          },
          ul: {
            listStyleType: 'disc',
            marginTop: theme('spacing.5'),
            marginBottom: theme('spacing.5'),
            paddingLeft: '1.625rem',
          },
          li: {
            marginTop: theme('spacing.2'),
            marginBottom: theme('spacing.2'),
          },
          ':is(ol, ul) > li': {
            paddingLeft: theme('spacing[1.5]'),
          },
          'ol > li::marker': {
            fontWeight: '400',
            color: 'var(--tw-prose-counters)',
          },
          'ul > li::marker': {
            color: 'var(--tw-prose-bullets)',
          },
          '> ul > li p': {
            marginTop: theme('spacing.3'),
            marginBottom: theme('spacing.3'),
          },
          '> ul > li > *:first-child': {
            marginTop: theme('spacing.5'),
          },
          '> ul > li > *:last-child': {
            marginBottom: theme('spacing.5'),
          },
          '> ol > li > *:first-child': {
            marginTop: theme('spacing.5'),
          },
          '> ol > li > *:last-child': {
            marginBottom: theme('spacing.5'),
          },
          'ul ul, ul ol, ol ul, ol ol': {
            marginTop: theme('spacing.3'),
            marginBottom: theme('spacing.3'),
          },

          // Horizontal rules
          hr: {
            borderColor: 'var(--tw-prose-hr)',
            borderTopWidth: 1,
            marginTop: theme('spacing.16'),
            marginBottom: theme('spacing.16'),
            maxWidth: 'none',
            marginLeft: `calc(-1 * ${theme('spacing.4')})`,
            marginRight: `calc(-1 * ${theme('spacing.4')})`,
            '@screen sm': {
              marginLeft: `calc(-1 * ${theme('spacing.6')})`,
              marginRight: `calc(-1 * ${theme('spacing.6')})`,
            },
            '@screen lg': {
              marginLeft: `calc(-1 * ${theme('spacing.8')})`,
              marginRight: `calc(-1 * ${theme('spacing.8')})`,
            },
          },

          // Quotes
          blockquote: {
            fontWeight: '500',
            fontStyle: 'italic',
            color: 'var(--tw-prose-quotes)',
            borderLeftWidth: '0.25rem',
            borderLeftColor: 'var(--tw-prose-quote-borders)',
            quotes: '"\\\\201C""\\\\201D""\\\\2018""\\\\2019"',
            marginTop: theme('spacing.8'),
            marginBottom: theme('spacing.8'),
            paddingLeft: theme('spacing.5'),
          },
          'blockquote p:first-of-type::before': {
            content: 'open-quote',
          },
          'blockquote p:last-of-type::after': {
            content: 'close-quote',
          },

          // Headings
          h1: {
            color: 'var(--tw-prose-headings)',
            fontWeight: '700',
            fontSize: theme('fontSize.2xl')[0],
            ...theme('fontSize.2xl')[1],
            marginBottom: theme('spacing.2'),
          },
          h2: {
            color: 'var(--tw-prose-headings)',
            fontWeight: '600',
            fontSize: theme('fontSize.lg')[0],
            ...theme('fontSize.lg')[1],
            marginTop: theme('spacing.16'),
            marginBottom: theme('spacing.2'),
          },
          h3: {
            color: 'var(--tw-prose-headings)',
            fontSize: theme('fontSize.base')[0],
            ...theme('fontSize.base')[1],
            fontWeight: '600',
            marginTop: theme('spacing.10'),
            marginBottom: theme('spacing.2'),
          },

          // Media
          'img, video, figure': {
            marginTop: theme('spacing.8'),
            marginBottom: theme('spacing.8'),
          },
          'figure > *': {
            marginTop: '0',
            marginBottom: '0',
          },
          figcaption: {
            color: 'var(--tw-prose-captions)',
            fontSize: theme('fontSize.xs')[0],
            ...theme('fontSize.xs')[1],
            marginTop: theme('spacing.2'),
          },

          // Tables
          table: {
            width: '100%',
            tableLayout: 'auto',
            textAlign: 'left',
            marginTop: theme('spacing.8'),
            marginBottom: theme('spacing.8'),
            lineHeight: theme('lineHeight.6'),
          },
          thead: {
            borderBottomWidth: '1px',
            borderBottomColor: 'var(--tw-prose-th-borders)',
          },
          'thead th': {
            color: 'var(--tw-prose-headings)',
            fontWeight: '600',
            verticalAlign: 'bottom',
            paddingRight: theme('spacing.2'),
            paddingBottom: theme('spacing.2'),
            paddingLeft: theme('spacing.2'),
          },
          'thead th:first-child': {
            paddingLeft: '0',
          },
          'thead th:last-child': {
            paddingRight: '0',
          },
          'tbody tr': {
            borderBottomWidth: '1px',
            borderBottomColor: 'var(--tw-prose-td-borders)',
          },
          'tbody tr:last-child': {
            borderBottomWidth: '0',
          },
          'tbody td': {
            verticalAlign: 'baseline',
          },
          tfoot: {
            borderTopWidth: '1px',
            borderTopColor: 'var(--tw-prose-th-borders)',
          },
          'tfoot td': {
            verticalAlign: 'top',
          },
          ':is(tbody, tfoot) td': {
            paddingTop: theme('spacing.2'),
            paddingRight: theme('spacing.2'),
            paddingBottom: theme('spacing.2'),
            paddingLeft: theme('spacing.2'),
          },
          ':is(tbody, tfoot) td:first-child': {
            paddingLeft: '0',
          },
          ':is(tbody, tfoot) td:last-child': {
            paddingRight: '0',
          },

          // Inline elements
          a: {
            color: 'var(--tw-prose-links)',
            textDecoration: 'underline transparent',
            fontWeight: '500',
            transitionProperty: 'color, text-decoration-color',
            transitionDuration: theme('transitionDuration.DEFAULT'),
            transitionTimingFunction: theme('transitionTimingFunction.DEFAULT'),
            '&:hover': {
              color: 'var(--tw-prose-links-hover)',
              textDecorationColor: 'var(--tw-prose-links-underline)',
            },
          },
          ':is(h1, h2, h3) a': {
            fontWeight: 'inherit',
          },
          strong: {
            color: 'var(--tw-prose-bold)',
            fontWeight: '600',
          },
          ':is(a, blockquote, thead th) strong': {
            color: 'inherit',
            fontWeight: 'inherit',
          },
          code: {
            color: 'var(--tw-prose-code)',
            borderRadius: theme('borderRadius.lg'),
            paddingTop: theme('padding.1'),
            paddingRight: theme('padding[1.5]'),
            paddingBottom: theme('padding.1'),
            paddingLeft: theme('padding[1.5]'),
            boxShadow: 'inset 0 0 0 1px var(--tw-prose-code-ring)',
            backgroundColor: 'var(--tw-prose-code-bg)',
            fontSize: theme('fontSize.2xs')[0],
          },
          ':is(a, h1, h2, h3, blockquote, thead th) code': {
            color: 'inherit',
            fontWeight: 'inherit',
          },
          'h2 code': {
            fontSize: theme('fontSize.base')[0],
            fontWeight: 'inherit',
          },
          'h3 code': {
            fontSize: theme('fontSize.sm')[0],
            fontWeight: 'inherit',
          },

          // Overrides
          ':is(h1, h2, h3) + *': {
            marginTop: '0',
          },
          '> :first-child': {
            marginTop: '0 !important',
          },
          '> :last-child': {
            marginBottom: '0 !important',
          },
        },
      },
      invert: {
        css: {
          '--tw-prose-body': 'var(--tw-prose-invert-body)',
          '--tw-prose-headings': 'var(--tw-prose-invert-headings)',
          '--tw-prose-links': 'var(--tw-prose-invert-links)',
          '--tw-prose-links-hover': 'var(--tw-prose-invert-links-hover)',
          '--tw-prose-links-underline':
            'var(--tw-prose-invert-links-underline)',
          '--tw-prose-bold': 'var(--tw-prose-invert-bold)',
          '--tw-prose-counters': 'var(--tw-prose-invert-counters)',
          '--tw-prose-bullets': 'var(--tw-prose-invert-bullets)',
          '--tw-prose-hr': 'var(--tw-prose-invert-hr)',
          '--tw-prose-quotes': 'var(--tw-prose-invert-quotes)',
          '--tw-prose-quote-borders': 'var(--tw-prose-invert-quote-borders)',
          '--tw-prose-captions': 'var(--tw-prose-invert-captions)',
          '--tw-prose-code': 'var(--tw-prose-invert-code)',
          '--tw-prose-code-bg': 'var(--tw-prose-invert-code-bg)',
          '--tw-prose-code-ring': 'var(--tw-prose-invert-code-ring)',
          '--tw-prose-th-borders': 'var(--tw-prose-invert-th-borders)',
          '--tw-prose-td-borders': 'var(--tw-prose-invert-td-borders)',
        },
      },
    }),"""
    )


    # 13. Hero Pattern (Updated Colors)
    # Replace HeroPattern component
    tool.replace_in_file(
        'src/components/HeroPattern.jsx',
        r'export function HeroPattern\(\) \{[\s\S]*?\}',
        """export function HeroPattern() {
  return (
    <div className="absolute inset-0 -z-10 mx-0 max-w-none overflow-hidden">
      <div className="absolute top-0 left-1/2 -ml-152 h-100 w-325 dark:mask-[linear-gradient(white,transparent)]">
        <div className="absolute inset-0 bg-linear-to-r from-[#757272] to-[#4e5244] mask-[radial-gradient(farthest-side_at_top,white,transparent)] opacity-40 dark:from-[#757272]/30 dark:to-[#4e5244]/30 dark:opacity-100">
          <GridPattern
            width={72}
            height={56}
            x={-12}
            y={4}
            squares={[
              [4, 3],
              [2, 1],
              [7, 3],
              [10, 6],
            ]}
            className="absolute inset-x-0 inset-y-[-50%] h-[200%] w-full skew-y-[-18deg] fill-black/40 stroke-black/50 mix-blend-overlay dark:fill-white/2.5 dark:stroke-white/5"
          />
        </div>
        <svg
          viewBox="0 0 1113 440"
          aria-hidden="true"
          className="absolute top-0 left-1/2 -ml-76 w-278.25 fill-white blur-[26px] dark:hidden"
        >
          <path d="M.016 439.5s-9.5-300 434-300S882.516 20 882.516 20V0h230.004v439.5H.016Z" />
        </svg>
      </div>
    </div>
  )
}"""
    )


    # 14. Dependencies
    # Add remark-frontmatter and remark-mdx-frontmatter to package.json
    tool.replace_in_file(
        'package.json',
        r'"dependencies": \{',
        """"dependencies": {
    "remark-frontmatter": "^5.0.0",
    "remark-mdx-frontmatter": "^4.0.0","""
    )

    # 15. Frontmatter Mapping Plugin
    # Create remark-frontmatter-metadata.mjs
    tool.write_file('src/mdx/remark-frontmatter-metadata.mjs', """import { visit } from 'unist-util-visit'

export function remarkMapFrontmatterMetadata() {
    return (tree) => {
        let hasMetadataExport = false
        let frontmatterMetadataNode = null
        let frontmatterMetadataIdentifier = null

        // First pass: Check for existing metadata export and find the frontmatterMetadata identifier
        visit(tree, 'mdxjsEsm', (node) => {
            const program = node.data?.estree
            if (!program || !program.body) return

            for (const statement of program.body) {
                if (
                    statement.type === 'ExportNamedDeclaration' &&
                    statement.declaration?.type === 'VariableDeclaration'
                ) {
                    for (const decl of statement.declaration.declarations) {
                        if (decl.id?.type === 'Identifier') {
                            if (decl.id.name === 'metadata') {
                                hasMetadataExport = true
                            }
                            if (decl.id.name === 'frontmatterMetadata') {
                                frontmatterMetadataNode = node
                                frontmatterMetadataIdentifier = decl.id
                            }
                        }
                    }
                }
            }
        })

        // Second pass: Rename if safe
        if (!hasMetadataExport && frontmatterMetadataIdentifier) {
            frontmatterMetadataIdentifier.name = 'metadata'
            // Sync value string to ensure tools not using ESTree also see the change
            if (frontmatterMetadataNode.value) {
                frontmatterMetadataNode.value = frontmatterMetadataNode.value.replace(
                    /\\bfrontmatterMetadata\\b/,
                    'metadata'
                )
            }
        }
    }
}
""")

    # 16. Auto-Metadata Plugin
    # Create remark-auto-metadata.mjs plugin
    tool.write_file('src/mdx/remark-auto-metadata.mjs', """import { visit } from 'unist-util-visit'
import { toString } from 'mdast-util-to-string'
import * as fs from 'node:fs'
import * as path from 'node:path'

export function remarkAutoMetadata() {
  return (tree, file) => {
    let title = null
    let description = null
    let metadataExportNode = null
    
    // 1. Find Title (H1) and Description (First Paragraph)
    let foundH1 = false
    visit(tree, (node) => {
      if (!title && node.type === 'heading' && node.depth === 1) {
        title = toString(node)
        foundH1 = true
        return 'skip'
      }

      if (foundH1 && !description && node.type === 'paragraph') {
        description = toString(node).slice(0, 160).trim()
        if (description.length === 160) description += '...'
        return 'skip'
      }
      
      // Check ESTree for exports
      if (node.type === 'mdxjsEsm') {
         const program = node.data?.estree
         if (program?.body) {
             for (const statement of program.body) {
                 if (statement.type === 'ExportNamedDeclaration' && statement.declaration?.declarations) {
                     for (const decl of statement.declaration.declarations) {
                         if (decl.id.name === 'metadata' || decl.id.name === 'frontmatterMetadata') {
                             metadataExportNode = node
                         }
                     }
                 }
             }
         }
      }
    })
    
    // Get file dates from file.history or file.path
    let filePath = file.history?.[0] || file.path
    let dateCreated = null
    let dateModified = null
    
    if (filePath && typeof filePath === 'string') {
      // Ensure path is absolute for fs.statSync to avoid issues with different loaders
      if (!path.isAbsolute(filePath)) {
          filePath = path.resolve(process.cwd(), filePath)
      }

      try {
        if (fs.existsSync(filePath)) {
            const stats = fs.statSync(filePath)
            dateCreated = stats.birthtime.toISOString().split('T')[0]
            dateModified = stats.mtime.toISOString().split('T')[0]
        }
      } catch (e) {
        // Silently fail if we can't read file stats
      }
    }
    
    // Use dateModified as the primary 'date' if available, otherwise dateCreated
    const primaryDate = dateModified || dateCreated
    
    if (metadataExportNode) {
        // We need to inject into the ESTree
        const program = metadataExportNode.data?.estree
        if (program?.body) {
            for (const statement of program.body) {
                if (statement.type === 'ExportNamedDeclaration' && statement.declaration?.declarations) {
                     for (const decl of statement.declaration.declarations) {
                        if (decl.id.name === 'metadata' || decl.id.name === 'frontmatterMetadata') {
                            // Handle undefined or null init (empty frontmatter case)
                            if (!decl.init || (decl.init.type === 'Identifier' && decl.init.name === 'undefined')) {
                                decl.init = {
                                    type: 'ObjectExpression',
                                    properties: []
                                }
                            }
                            
                            if (decl.init?.type === 'ObjectExpression') {
                                const properties = decl.init.properties
                                
                                const hasTitle = properties.some(p => (p.key?.name === 'title' || p.key?.value === 'title'))
                                const hasDescription = properties.some(p => (p.key?.name === 'description' || p.key?.value === 'description'))
                                const hasDate = properties.some(p => (p.key?.name === 'date' || p.key?.value === 'date'))
                                const hasDateCreated = properties.some(p => (p.key?.name === 'dateCreated' || p.key?.value === 'dateCreated'))
                                const hasDateModified = properties.some(p => (p.key?.name === 'dateModified' || p.key?.value === 'dateModified'))
                                
                                // Auto-infer title and description
                                if (!hasTitle && title) {
                                    properties.push({
                                        type: 'Property',
                                        key: { type: 'Identifier', name: 'title' },
                                        value: { type: 'Literal', value: title },
                                        kind: 'init'
                                    })
                                }
                                
                                if (!hasDescription && description) {
                                     properties.push({
                                        type: 'Property',
                                        key: { type: 'Identifier', name: 'description' },
                                        value: { type: 'Literal', value: description },
                                        kind: 'init'
                                    })
                                }
                                
                                // Add file dates if available
                                if (!hasDate && primaryDate) {
                                    properties.push({
                                        type: 'Property',
                                        key: { type: 'Identifier', name: 'date' },
                                        value: { type: 'Literal', value: primaryDate },
                                        kind: 'init'
                                    })
                                }

                                if (!hasDateCreated && dateCreated) {
                                    properties.push({
                                        type: 'Property',
                                        key: { type: 'Identifier', name: 'dateCreated' },
                                        value: { type: 'Literal', value: dateCreated },
                                        kind: 'init'
                                    })
                                }
                                
                                if (!hasDateModified && dateModified) {
                                    properties.push({
                                        type: 'Property',
                                        key: { type: 'Identifier', name: 'dateModified' },
                                        value: { type: 'Literal', value: dateModified },
                                        kind: 'init'
                                    })
                                }

                                // Sync value string if possible
                                if (metadataExportNode.value) {
                                    // This is a naive sync, but better than nothing
                                    if (!hasTitle && title && !metadataExportNode.value.includes('title:')) {
                                        metadataExportNode.value = metadataExportNode.value.replace(/}\\s*$/, `, title: ${JSON.stringify(title)} }`)
                                    }
                                    if (!hasDescription && description && !metadataExportNode.value.includes('description:')) {
                                        metadataExportNode.value = metadataExportNode.value.replace(/}\\s*$/, `, description: ${JSON.stringify(description)} }`)
                                    }
                                    if (!hasDate && primaryDate && !metadataExportNode.value.includes('date:')) {
                                        metadataExportNode.value = metadataExportNode.value.replace(/}\\s*$/, `, date: ${JSON.stringify(primaryDate)} }`)
                                    }
                                    // Clean up potential ", }" at start of object
                                    metadataExportNode.value = metadataExportNode.value.replace(/\\{\\s*,\\s*/, '{ ')
                                }
                            }
                        }
                     }
                }
            }
        }
    } else if (title || description || primaryDate) {
         const properties = []
         
         if (title) {
             properties.push({
                 type: 'Property',
                 key: { type: 'Identifier', name: 'title' },
                 value: { type: 'Literal', value: title },
                 kind: 'init'
             })
         }
         
         if (description) {
             properties.push({
                 type: 'Property',
                 key: { type: 'Identifier', name: 'description' },
                 value: { type: 'Literal', value: description },
                 kind: 'init'
             })
         }

         if (primaryDate) {
            properties.push({
                type: 'Property',
                key: { type: 'Identifier', name: 'date' },
                value: { type: 'Literal', value: primaryDate },
                kind: 'init'
            })
         }
         
         if (dateCreated) {
             properties.push({
                 type: 'Property',
                 key: { type: 'Identifier', name: 'dateCreated' },
                 value: { type: 'Literal', value: dateCreated },
                 kind: 'init'
             })
         }
         
         if (dateModified) {
             properties.push({
                 type: 'Property',
                 key: { type: 'Identifier', name: 'dateModified' },
                 value: { type: 'Literal', value: dateModified },
                 kind: 'init'
             })
         }
         
         const valueString = properties.map(p => `${p.key.name}: ${JSON.stringify(p.value.value)}`).join(', ')
         
         tree.children.unshift({
            type: 'mdxjsEsm',
            value: `export const metadata = { ${valueString} }`,
            data: {
                estree: {
                    type: 'Program',
                    sourceType: 'module',
                    body: [
                        {
                            type: 'ExportNamedDeclaration',
                            specifiers: [],
                            source: null,
                            declaration: {
                                type: 'VariableDeclaration',
                                kind: 'const',
                                declarations: [
                                    {
                                        type: 'VariableDeclarator',
                                        id: { type: 'Identifier', name: 'metadata' },
                                        init: {
                                            type: 'ObjectExpression',
                                            properties: properties
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
         })
    }
  }
}
""")

    # 17. MDX Config
    # Update remark.mjs to use frontmatter and auto-metadata plugins
    tool.write_file('src/mdx/remark.mjs', """import { mdxAnnotations } from 'mdx-annotations'
import remarkFrontmatter from 'remark-frontmatter'
import remarkMdxFrontmatter from 'remark-mdx-frontmatter'
import { remarkMapFrontmatterMetadata } from './remark-frontmatter-metadata.mjs'
import { remarkAutoMetadata } from './remark-auto-metadata.mjs'
import remarkGfm from 'remark-gfm'

export const remarkPlugins = [
  mdxAnnotations.remark,
  remarkFrontmatter,
  [remarkMdxFrontmatter, { name: 'frontmatterMetadata' }],
  remarkMapFrontmatterMetadata,
  remarkAutoMetadata,
  remarkGfm,
]
""")

    print("\nRebranding complete!")

if __name__ == "__main__":
    run_rebrand()
