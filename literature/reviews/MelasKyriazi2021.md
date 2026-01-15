---
citekey: "MelasKyriazi2021"
title: "Do You Even Need Attention? A Stack of Feed-Forward Layers Does Surprisingly Well on ImageNet"
authors: ['Luke Melas-Kyriazi']
year: 2021
venue: "arXiv"
status: "Inbox"
tags: []
---

# Abstract
The strong performance of vision transformers on image classification and other vision tasks is often attributed to the design of their multi-head attention layers. However, the extent to which attention is responsible for this strong performance remains unclear. In this short report, we ask: is the attention layer even necessary? Specifically, we replace the attention layer in a vision transformer with a feed-forward layer applied over the patch dimension. The resulting architecture is simply a series of feed-forward layers applied over the patch and feature dimensions in an alternating fashion. In experiments on ImageNet, this architecture performs surprisingly well: a ViT/DeiT-base-sized model obtains 74.9\% top-1 accuracy, compared to 77.9\% and 79.9\% for ViT and DeiT respectively. These results indicate that aspects of vision transformers other than attention, such as the patch embedding, may be more responsible for their strong performance than previously thought. We hope these results prompt the community to spend more time trying to understand why our current models are as effective as they are.

# Key Findings
- **Attention is optional**: Replacing the Multi-Head Attention (MHA) layer in ViT with a simple Feed-Forward layer over the patch dimension yields **74.9% top-1 accuracy** on ImageNet (vs 77.9% for ViT).
- **Critical Insight**: The strong performance of Transformers may be driven more by the **Patch Embedding** and modern **training recipe** (augmentations) than the attention mechanism itself.
- **Complexity**: The proposed "Feed-Forward-Only" model has linear complexity $O(N)$ with sequence length, compared to $O(N^2)$ for attention.

# Methodology
- **Architecture**: A stack of "Linear Blocks".
- **Mechanism**: Alternates between:
    1.  **Mixing Features**: Standard MLP applied to each token independently (channel mixing).
    2.  **Mixing Patches**: MLP applied across the patch dimension (spatial mixing).
- **Core Implementation**:
```python
class LinearBlock(nn.Module):
    def __init__(self, dim, n_tokens=197, mlp_ratio=4.):
        super().__init__()
        # FF over features (Channel Mixing)
        self.mlp1 = Mlp(in_features=dim, hidden_features=int(dim*mlp_ratio))
        # FF over patches (Spatial Mixing)
        self.mlp2 = Mlp(in_features=n_tokens, hidden_features=int(n_tokens*mlp_ratio))

    def forward(self, x):
        # x shape: [Batch, Tokens, Dim]
        x = x + self.drop_path(self.mlp1(self.norm1(x)))
        x = x.transpose(-2, -1) # Transpose to mix [Batch, Dim, Tokens]
        x = x + self.drop_path(self.mlp2(self.norm2(x)))
        x = x.transpose(-2, -1) # Restore
        return x
```

# Relevance to Project
- [ ] **Simulation Efficiency**: If we are simulating large agent populations, this linear-complexity interaction model might be vastly more efficient than full attention.
- [ ] **Hypothesis Testing**: Supports the hypothesis that *local* interactions (or fixed mixing) are sufficient for emergence, without dynamic attention routing.
