const tabsContainer = document.querySelector(".tabs-container");
const tabList = tabsContainer.querySelector("ul");
const tabButtons = tabList.querySelectorAll("a");
const tabPanels = Array.from(tabsContainer.querySelectorAll(".tabs__panels > div"));

tabButtons.forEach((tab, index) => {
    if (index !== 0) {
        tabPanels[index].setAttribute("hidden", "");
    }
});

tabsContainer.addEventListener("click", (e) => {
    const clickedTab = e.target.closest("a");
    if (!clickedTab) return;
    e.preventDefault();

    const activePanelId = clickedTab.getAttribute("href");
    const activePanel = tabsContainer.querySelector(activePanelId);

    if (activePanel) {
        tabPanels.forEach((panel) => {
            panel.setAttribute("hidden", "");
        });
    
        activePanel.removeAttribute("hidden");
    }
});